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
        table_name='tb_study_quality_output',
        push_down_predicate='partition'
        )
    
    print('verify schema input')
    dyf_input.printSchema()
    
    return dyf_input

def apply_quality(dyf):
    ruleset = """
        Rules = [
        ColumnExists "col_1",
        IsComplete "col_2"
        ]"""
    
    print(f'apply quality rules {ruleset}')
    dqResults = EvaluateDataQuality.apply(
        frame=dyf,
        ruleset=ruleset,
        publishing_options={
            "dataQualityEvaluationContext": "dqResults",
            "enableDataQualityCloudWatchMetrics": True,
            "enableDataQualityResultsPublishing": True,
            "resultsS3Prefix": "s3://bkt-key/spec/output_quality/job_x/",
        },
    )
    
    print(boto3.__version__)
    session = boto3.session.Session()
    client = session.client('glue')
    
    response_list_data_quality_ruleset_evaluation_runs_listss = client.list_data_quality_ruleset_evaluation_runs()
    print(f' result response_list_data_quality_ruleset_evaluation_runs_listss -- \n {response_list_data_quality_ruleset_evaluation_runs_listss}')
    
    response_get_data_quality_ruleset = client.get_data_quality_ruleset(Name='dqResults')
    print(f' result get_data_quality_ruleset -- \n {response_get_data_quality_ruleset}')
    
    # response = client.get_data_quality_result(ResultId='jr_')
    
    '''
    response = client.batch_get_data_quality_result(
        ResultIds=[
            'id',
        ]
    )
    
    # response = client.list_jobs()
    '''
    response_list_data_quality_ruleset_evaluation_runs = client.list_data_quality_results(
        Filter={
            'DataSource': {
                'GlueTable': {
                    'DatabaseName': 'db_workspace',
                    'TableName': 'tb_study_quality_output'
                }
            },
            'JobName': 'job_test_data_quality_glue'
        })
    print(f' result list_data_quality_results -- \n {response_list_data_quality_results}')
        
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
    
    print('boto3.__version__')
    print(boto3.__version__)
    dyf_input = load_table(glueContext)
    
    df_validated, dq_validated = apply_quality(dyf_input)
    
    print('select')
    df_x = dq_validated.select("Rule","Outcome").show()

    print('load')
    df_id = spark.read.csv("s3://bkt-key/sor/output_quality/job_x/", header=True)
    df_id.show(3, truncate=False)
    
    
    '''
    my_var = "id_xpto"

    result = {
        "job_result": "Concluído com sucesso",
        "my_var": my_var
    }

    '''
    job.commit()
    
if __name__ == '__main__':
    main()
