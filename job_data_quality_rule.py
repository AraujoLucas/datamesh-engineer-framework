import sys
import json
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import lit
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from awsgluedq.transforms import EvaluateDataQuality
import boto3
from datetime import datetime

def extract_rules_payload(rules):
    formatted_rules = [f'{list(rule.keys())[0]} "{list(rule.values())[0]}"' for rule in rules]
    payload = "Rules = [\n{}\n]".format(',\n'.join(formatted_rules))
    return payload

def extract_params(each_params):
    job_name = each_params.get('JOB_NAME', '')
    source_database = each_params.get('sourcer_database', '')
    source_table = each_params.get('source_table', '')
    partition_key = each_params.get('partition_key', '')
    rules = extract_rules_payload(each_params.get('data_quality_rules', []))
    stage = each_params.get('stage', '')
    jornada = each_params.get('jornada', '')
    output_database = each_params.get('output_database', '')
    output_table = each_params.get('output_table', '')
    print(f"job_name: {job_name}\n"
          f"Database Source: {source_database}\n"
          f"Table Source: {source_table}\n"
          f"Partition: {partition_key}\n"
          f"Rules: {rules}\n"
          f"Stage: {stage}\n"
          f"Jornada: {jornada}\n"
          f"Database target: {output_database}\n"
          f"Table Target: {output_table}")
    return job_name,source_database,source_table,\
    partition_key,rules,stage,jornada,output_database,output_table

def load_table(glueContext,source_database,source_table,partition_key):
    print(f'{datetime.now()} ::: starting data load  :::')
    dyf_input = glueContext.create_dynamic_frame.from_catalog(
        database=source_database,
        table_name=source_table,
        push_down_predicate=f'anomesdia={partition_key}'
        )
    print(f'{datetime.now()} ::: end of data loading  :::')
    dyf_input.show(3)
    return dyf_input

def apply_quality(dyf_table_input,rules):
    ruleset = f"""{rules}"""
    print(f'apply quality rules {ruleset}')
    dyf_results_quality = EvaluateDataQuality.apply(
        frame=dyf_table_input,
        ruleset=ruleset,
        publishing_options={
            "dataQualityEvaluationContext": "ruleset_jornada_1",
            "enableDataQualityCloudWatchMetrics": True,
            "enableDataQualityResultsPublishing": True
        },
    )
    return dyf_results_quality

def format_df(job_name,source_table,dyf_results_quality,stage,jornada,partition_key):
    df = dyf_results_quality.toDF()
    df_quality_full = df.withColumn("job_name", lit(job_name))\
            .withColumn("table_name", lit(source_table))\
            .withColumnRenamed("Rule", "rule_name")\
            .withColumnRenamed("Outcome", "status")\
            .withColumn("stage", lit(stage))\
            .withColumn("jornada", lit(jornada))\
            .withColumn("anomesdia", lit(partition_key))\
            .select('job_name','table_name','rule_name',\
                    'status','stage','jornada','anomesdia')
    df_quality_full.show(5, truncate=False)
    return df_quality_full

def write_catalog(glueContext,output_database,output_table,df_quality_results):
    dyf_results_quality = DynamicFrame.fromDF(
        df_quality_results, glueContext, "dyf_results_quality")
    print(f'{datetime.now()} ::: starting data write in catalog :::')
    glueContext.write_dynamic_frame.from_catalog(
        frame = dyf_results_quality,
        database = output_database,
        table_name = output_table,
        additional_options={
            "partitionKeys": ["anomesdia"]
        }
    )
    return print(f'{datetime.now()} ::: finished recording data in the catalog :::')

def main():
    print(f'{datetime.now()} ::: start job :::')
    glue_params = getResolvedOptions(sys.argv, ['JOB_NAME','glue_params'])
    print(f'{datetime.now()} ::: params ::: {glue_params}')
    
    sc = SparkContext()
    glueContext = GlueContext(sc.getOrCreate())
    spark = glueContext.spark_session
    job = Job(glueContext)

    job.init(glue_params['JOB_NAME'], glue_params)
    
    for each_param in json.loads(glue_params["glue_params"]):    
         print(f'{datetime.now()} ::: initializing glue job with job params {each_param}\n')
       
         print(f'{datetime.now()} ::: running task extract params for job :::')
         job_name,source_database,source_table,partition_key,\
         rules,stage,jornada,output_database,output_table = extract_params(each_param)
         
         print(f'{datetime.now()} ::: running task load data :::')
         dyf_table_input = load_table(glueContext,source_database,source_table,partition_key)
         
         print(f'{datetime.now()} ::: running task apply quality rule :::')
         dyf_results_quality = apply_quality(dyf_table_input,rules)

         print(f'{datetime.now()} ::: running taks formating results quality :::')
         df_quality_results = format_df(job_name,source_table,dyf_results_quality,stage,jornada,partition_key)
        
         print(f'{datetime.now()} ::: running task write in catalog :::')
         write_catalog(glueContext,output_database,output_table,df_quality_results)

    job.commit()
    
if __name__ == '__main__':
    main()
