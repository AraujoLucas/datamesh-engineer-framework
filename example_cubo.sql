drop table tb_cliente
create external table if not exists tb_clientes (
    cod_id_cliente STRING,
    ds_nome STRING,
    ds_segmento STRING,
    ds_origem_jornada STRING,
    ds_canal_entrada STRING,
    dt_abertura_conta STRING,
    ds_status_cliente STRING,
    effective_date TIMESTAMP,
    end_date TIMESTAMP,
    current_flag STRING
)
PARTITIONED BY (anomesdia STRING)
LOCATION 's3://bkt/spec/tb_clientes';
show create table tb_clientes

drop table tb_carteira
create external table if not exists tb_carteira (
    cod_id_carteira STRING,
    ds_nome_carteira STRING,
    ds_tipo_carteira STRING,
    dt_criacao STRING,
    vl_total_investido DOUBLE,
    vl_retornos DOUBLE,
    effective_date TIMESTAMP,
    end_date TIMESTAMP,
    current_flag STRING
)
PARTITIONED BY (anomesdia STRING)
LOCATION 's3://bkt/spec/tb_carteira';

drop table tb_movimentacoes
create external table if not exists tb_movimentacoes (
    cod_id_movimentacao STRING,
    cod_id_cliente STRING,
    cod_id_produto STRING,
    ds_tipo_transacao STRING,
    vl_transacao DOUBLE,
    dt_transacao STRING
)
PARTITIONED BY (anomesdia STRING)
LOCATION 's3://bkt/spec/tb_movimentacoes';


insert into tb_clientes
values
    ('1', 'Cliente A', 'Segmento X', 'Origem A', 'Canal 1', '2024-07-14', 'Ativo', TIMESTAMP '2024-07-14 10:00:00', null, 'Y', '20240714'),
    ('2', 'Cliente B', 'Segmento Y', 'Origem B', 'Canal 2', '2024-07-14', 'Ativo', TIMESTAMP '2024-07-14 11:00:00', null, 'Y', '20240714'),
    ('3', 'Cliente C', 'Segmento Z', 'Origem C', 'Canal 3', '2024-07-14', 'Inativo', TIMESTAMP '2024-07-14 12:00:00', null, 'N', '20240714');
insert into tb_movimentacoes
values
    ('201', '1', 'P1001', 'Compra', 150.00, '2024-07-14', '20240714'),
    ('202', '2', 'P1002', 'Venda', 200.00, '2024-07-14', '20240714'),
    ('203', '3', 'P1003', 'Transferência', 50.00, '2024-07-14', '20240714');
    
insert into tb_carteira
values
    ('101', 'Carteira A', 'Conservadora', '2024-07-14', 50000.00, 2500.00, TIMESTAMP '2024-07-14 10:00:00', null, 'Y', '20240714'),
    ('102', 'Carteira B', 'Moderada', '2024-07-14', 75000.00, 4500.00, TIMESTAMP '2024-07-14 11:00:00', null, 'Y', '20240714'),
    ('103', 'Carteira C', 'Agressiva', '2024-07-14', 100000.00, 8000.00, TIMESTAMP '2024-07-14 12:00:00', TIMESTAMP '2024-07-15 08:00:00', 'N', '20240714');

with cliente as(
select
*
from tb_clientes
--where anomesdia = '20240714'
),
movimentacao as (
select *
from tb_movimentacoes
--where anomesdia = '20240714'
)
select 
* 
from cliente tb1
join movimentacao tb2
on tb1.cod_id_cliente = tb2.cod_id_cliente
where tb2.anomesdia = '20240717'



import matplotlib.pyplot as plt
import numpy as np

# Dados fictícios para contas abertas, ativações no M0 e erros
meses = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
contas_abertas = np.array([1000, 1200, 1500, 1300, 1600, 1700])
ativacoes_m0 = np.array([400, 500, 550, 480, 600, 650])
erros_ativos = np.array([50, 55, 60, 48, 70, 75])
erros_nao_ativos = np.array([200, 300, 400, 380, 450, 480])

# Percentual de ativação no M0
percentual_ativacao_m0 = (ativacoes_m0 / contas_abertas) * 100

# Gráfico de Barras Empilhadas - Percentual de Ativação no M0
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(meses, percentual_ativacao_m0, color='green', label='Ativados')
ax.bar(meses, 100 - percentual_ativacao_m0, bottom=percentual_ativacao_m0, color='red', label='Não Ativados')

ax.set_xlabel('Meses')
ax.set_ylabel('Percentual (%)')
ax.set_title('Percentual de Ativação no M0 em Relação ao Total de Contas Abertas')
ax.legend()

plt.tight_layout()
plt.show()

# Gráfico de Linhas - Percentual de Erros MoM
fig, ax = plt.subplots(figsize=(10, 6))
percentual_erros_ativos = (erros_ativos / ativacoes_m0) * 100
percentual_erros_nao_ativos = (erros_nao_ativos / (contas_abertas - ativacoes_m0)) * 100

ax.plot(meses, percentual_erros_ativos, marker='o', color='blue', label='Ativados com Erros')
ax.plot(meses, percentual_erros_nao_ativos, marker='o', color='orange', label='Não Ativados com Erros')

ax.set_xlabel('Meses')
ax.set_ylabel('Percentual de Erros (%)')
ax.set_title('Percentual de Erros MoM: Ativados vs Não Ativados')
ax.legend()

plt.tight_layout()
plt.show()


