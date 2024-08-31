import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Dados de cohort de erros
cohort_erro_data = {
    'Mês de Ativação': ['Mai', 'Mai', 'Mai', 'Jun', 'Jun', 'Jul'],
    'Mês': ['M0', 'M1', 'M2', 'M0', 'M1', 'M0'],
    'Percentual de Erros (%)': [56.8, 78.12, 73.62, 62.22, 77.76, 62.55]
}

# Dados de cohort de transações
cohort_transacao_data = {
    'Mês de Ativação': ['Mai', 'Mai', 'Mai', 'Jun', 'Jun', 'Jul'],
    'Mês': ['M0', 'M1', 'M2', 'M0', 'M1', 'M0'],
    'Percentual de Transações (%)': [76.58, 89.06, 84.04, 76.1, 88.49, 77.86]
}

# Criar DataFrames
df_cohort_erro = pd.DataFrame(cohort_erro_data)
df_cohort_transacao = pd.DataFrame(cohort_transacao_data)

# Invertendo a ordem dos meses de ativação
df_cohort_erro['Mês de Ativação'] = pd.Categorical(df_cohort_erro['Mês de Ativação'], categories=['Jul', 'Jun', 'Mai'], ordered=True)
df_cohort_transacao['Mês de Ativação'] = pd.Categorical(df_cohort_transacao['Mês de Ativação'], categories=['Jul', 'Jun', 'Mai'], ordered=True)

# Invertendo novamente a ordem dos meses de ativação para Mai -> Jun -> Jul
df_cohort_erro['Mês de Ativação'] = pd.Categorical(df_cohort_erro['Mês de Ativação'], categories=['Mai', 'Jun', 'Jul'], ordered=True)
df_cohort_transacao['Mês de Ativação'] = pd.Categorical(df_cohort_transacao['Mês de Ativação'], categories=['Mai', 'Jun', 'Jul'], ordered=True)

# Configurar gráfico de heatmap para cohort de erros com a ordem corrigida
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
cohort_erro_pivot = df_cohort_erro.pivot(index='Mês de Ativação', columns='Mês', values='Percentual de Erros (%)')
sns.heatmap(cohort_erro_pivot, annot=True, fmt=".2f", cmap="Blues", linewidths=0.5)
plt.title('Cohort de Percentual de Erros')

# Configurar gráfico de heatmap para cohort de transações com a ordem corrigida
plt.subplot(1, 2, 2)
cohort_transacao_pivot = df_cohort_transacao.pivot(index='Mês de Ativação', columns='Mês', values='Percentual de Transações (%)')
sns.heatmap(cohort_transacao_pivot, annot=True, fmt=".2f", cmap="Greens", linewidths=0.5)
plt.title('Cohort de Percentual de Transações')

plt.tight_layout()
plt.show()


# Criando o DataFrame com os dados
data = {
    "M0": [62.2, 76.6],
    "M1": [77.1, 88.8],
    "M2": [73.6, 84.0]
}

df = pd.DataFrame(data, index=["--Média de Erros (%)", "--Média de Transações (%)"])

# Criando a matriz com heatmap em tons de azul
plt.figure(figsize=(8, 4))
sns.heatmap(df, annot=True, cmap="Blues", fmt=".1f", cbar=True)

# Adicionando título
plt.title("Matriz de Correlação entre Média de Erros e Transações")

# Exibindo o gráfico
plt.show()
