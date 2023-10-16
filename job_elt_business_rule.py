import boto3
import awswrangler as wr
import pandas as pd

def read_table(database, table,partition):
    query = f'SELECT * FROM {table} where {partition}'
    df = wr.athena.read_sql_query(query, database=database)
    return  
def process_data(df):
    print('df input')
    print(df.head(3))
    print(df.dtypes)
    df_string = df.astype(str)
    print('df ouput trasnformation')
    print(df_string.head(3))
    print(df_string.dtypes)
    return df_string

def write_table(df, database, tb_output,path):
    wr.s3.to_parquet(
        df=df,
        database=database,
        table=tb_output,
        dataset=True,
        path=path,
        partition_cols=['partition'],
        mode="overwrite"
    )

if __name__ == "__main__":
    db = 'db_workspace'
    tb_input = 'tb_study_quality_input'
    partition = 'partition'
    tb_output = 'tb_study_quality_output'
    s3_output = 's3://bkt-key/spec/'
    path =s3_output+tb_output

    df = read_table(db,tb_input,partition)
     
    df_clean = process_data(df)
    
    write_table(df_clean, db, tb_output, path)
