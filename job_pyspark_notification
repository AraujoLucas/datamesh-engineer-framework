import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import json
import boto3
from datetime import datetime
now = datetime.now()
date_process = "%d-%d-%02d-%02d:%02d:%02s" % (now.year, now.month, now.day, now.hour, now.minute, now.second)

def load_files(glueContext,spark, glue_params: dict):
    # extrac params
    db_target = glue_params['db_target']
    tb_target = glue_params['tb_target']
    account = glue_params['account-id']
    data_source_1 = glue_params['data_source_1']
    data_target = glue_params['data_target']
    now = datetime.now()
    date_process = "%s%02d%s" % (now.year, now.month,now.day)
    path_output = '%s/tb_teste_audit/parquet/dt=%s' % (data_target,date_process)
    
    print(f'{datetime.now()} --- Account {account}')
    print(f'{datetime.now()} --- Database target for load {db_target}')
    print(f'{datetime.now()} --- Table for ingeston {tb_target}')
    print(f'{datetime.now()} --- Data_source_1 input for load {data_source_1}')
    print(f'{datetime.now()} --- Data_target for load results {data_target}')
    
    print(f'{datetime.now()} --- Loading files from path {data_source_1}')
    df_users = read_json(data_source_1,spark)
    return df_users,db_target,tb_target,data_target,account

# function for read files in format json
def read_json(data_source,spark):
    print(f'{datetime.now()} - Initializing load in memory')
    df_json = spark.read.load(
        path=data_source,
        format='json')
    print(f'{datetime.now()} - DF load in memory')
    df_json.show(3)
    return df_json

def post_event_sns_audit_sor(data_target,tb_target,partition,date_process,client,account):
    arn = 'arn:aws:sns:region:%s:topic_test_notification' % (account)
    bkt_key = data_target+tb_target
    message = {
        "bkt_key": bkt_key, 
        "tb_name": tb_target, 
        "partition": partition, 
        "date_ingestion":date_process, 
        "status":"starting load", 
        "pf":"false"
    }
    print(f'payload: {message}')
    client = boto3.client('sns')
    response = client.publish(
        TargetArn=arn,
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json'
    )
    return print(response)

# function main the program
def main():
    partition = "%d-%d-%02d" % (now.year, now.month, now.day)
    sns_client = boto3.resource('sns')
    print(f'{datetime.now()} --- Solving arguments \n')
    glue_params = getResolvedOptions(sys.argv, ['JOB_NAME','glue_params'])
    print(f'{datetime.now()} --- Solved {glue_params} params\n')
    
    sc = SparkContext()
    glueContext = GlueContext(SparkContext.getOrCreate())
    spark = glueContext.spark_session
    job = Job(glueContext)

    job.init(glue_params['JOB_NAME'], glue_params)
    
    for each_param in json.loads(glue_params["glue_params"]):
        print(f'{datetime.now()} --- initializing glue job with job params {each_param}.\n')
        
        print(f'{datetime.now()} --- Initialing load files in memory')
        df_json,db_target,tb_target,data_target,account = load_files(glueContext,spark, each_param)
            
        print(f'{datetime.now()} --- persisting data in audit table')
        post_event_sns_audit_sor(data_target,tb_target,partition,date_process,sns_client,account)

    job.commit()

if __name__ == '__main__':
    main()
