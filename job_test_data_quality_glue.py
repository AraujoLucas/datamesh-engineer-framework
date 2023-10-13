import sys
import json
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from awsgluedq.transforms import EvaluateDataQuality
import boto3
from datetime import datetime

def format_df(dyf):
    df = dyf.toDF()
    df.show(3)
    return df

def load_table(glueContext):
    print('lendo DF')
    dyf_input = glueContext.create_dynamic_frame.from_catalog(
        database='db_workspace',
        table_name='tb_study_quality_v1',
        push_down_predicate='anomesdia=20231012'
        )
    
    print('verify schema input')
    dyf_input.printSchema()
    
    return dyf_input

def apply_quality(dyf):
    ruleset = """
        Rules = [
        ColumnExists "col_1",
        IsComplete "col_2",
        ColumnExists "col_2",
        IsComplete "col_3",
        ColumnExists "col_3",
        IsComplete "col_4",
        ColumnExists "col_4",
        IsComplete "col_5",
        ColumnExists "col_5",
        IsComplete "col_1",
        ColumnExists "anomesdia",
        IsComplete "anomesdia"
        ]"""
    
    print(f'apply quality rules {ruleset}')
    dqResults = EvaluateDataQuality.apply(
        frame=dyf,
        ruleset=ruleset,
        publishing_options={
            "dataQualityEvaluationContext": "dyf",
            "enableDataQualityCloudWatchMetrics": True,
            "enableDataQualityResultsPublishing": True,
            "resultsS3Prefix": "s3://bkt/output_quality/job_x/",
        },
    )
    
    print('format dyf to df')
    df_input_validated = format_df(dyf)
    df_input_validated.show()
    dq_validated = format_df(dqResults)
    dq_validated.show()

    return df_input_validated, dq_validated

def main():
    print(f'{datetime.now()} --- Init job \n')
    glue_params = getResolvedOptions(sys.argv, ['JOB_NAME','glue_params'])
    
    sc = SparkContext()
    glueContext = GlueContext(SparkContext.getOrCreate())
    spark = glueContext.spark_session
    job = Job(glueContext)

    job.init(glue_params['JOB_NAME'], glue_params)

    dyf_input = load_table(glueContext)
    
    df_validated, dq_validated = apply_quality(dyf_input)
    
    print('select')
    df_x = dq_validated.select("Rule","Outcome").show()
    '''
    print('load')
    df_id = spark.read.load("s3://bkt")
    df_id.show()
    print('select')
    df_x = df_id.select("dqRunId").show()
    '''
    my_var = "id_xpto"

    result = {
        "job_result": "Concluído com sucesso",
        "my_var": my_var
    }

  
    job.commit()
    
if __name__ == '__main__':
    main()
