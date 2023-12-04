-- ## scripts ddls for lab glue data quality
-- ####################### table input quality mock ####################### 
DROP EXTERNAL TABLE tb_data_input_study_quality
CREATE EXTERNAL TABLE tb_data_input_study_quality(
  id_cli int, 
  nome_cli string,
  estado_cli string,
  valor_pix_int double,
  valor_pix_out double) 
PARTITIONED BY (anomesdia int)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION
  's3://bkt/layer/tb_data_input_study_quality'
TBLPROPERTIES (
  'parquet.compress'='SNAPPY')

insert into tb_data_input_study_quality (id_cli, nome_cli, estado_cli, valor_pix_int, valor_pix_out, anomesdia)
values (1,'joao','são paulo',null,500.00,20231204),
        (2,'maria','parana',1000.00,1000.00,20231205),
        (3,'araujo','rio de janeiro',1000.00,00.00,20231205)

select * 
from tb_data_input_study_quality
where anomesdia = 20231204

select anomesdia, COUNT(*) as qntd_linhas
from tb_data_input_study_quality
group by anomesdia
order by qntd_linhas desc


-- ####################### table quality full ####################### 

CREATE EXTERNAL TABLE tb_quality_full_study(
  job_name string, 
  table_name string, 
  rule_name string, 
  status string,
  stage string,
  jornada string)
PARTITIONED BY (anomesdia int)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION
  's3://bkt/layer/tb_quality_full_study'
TBLPROPERTIES (
  'parquet.compress'='SNAPPY')
  

insert into tb_quality_full_study (job_name, table_name, rule_name, status, stage, jornada, anomesdia)
values -- ('job_1','table_1','rule_1','fail','origem','jornada_1',20231204),
        ('job_1','table_1','rule_2','success','origem','jornada_1',20231204),
        ('job_1','table_1','rule_3','success','origem','jornada_1',20231204),
        ('job_1','table_1','rule_4','success','origem','jornada_1',20231205)

-- count partitions
select anomesdia, COUNT(*) as qntd_linhas
from tb_quality_full_study
group by anomesdia
order by qntd_linhas desc

