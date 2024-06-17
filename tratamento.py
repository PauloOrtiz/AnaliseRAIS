import pandas as pd 

RaisBD = pd.read_csv('./src/data/raisbd.csv',sep=';',encoding='latin1',index_col=False)


RaisBD['salario_individual'] = RaisBD['massa_rendimentos'] / RaisBD['Emprego_formal']

RaisBD = RaisBD[RaisBD['salario_individual'] > 0]
RaisBD = RaisBD[RaisBD['EMP_C_SAL'] > 0]
RaisBD = RaisBD[RaisBD['massa_rendimentos'] > 0]

# Agrupar por ano e calcular as somas necessárias
agrupado = RaisBD.groupby('Ano').agg({
    'Emprego_formal': 'sum',
    'massa_rendimentos': 'sum'
}).reset_index()

# Calcular a média salarial por ano
agrupado['media_salarial'] = agrupado['massa_rendimentos'] / agrupado['Emprego_formal']

# Calcular o menor e maior salário individual por ano
menor_salario = RaisBD[RaisBD['Emprego_formal'] == 1].groupby('Ano')['salario_individual'].min().reset_index()
maior_salario = RaisBD.groupby('Ano')['salario_individual'].max().reset_index()

# Combinar os resultados em uma única tabela
analise_salarial = agrupado.merge(menor_salario, on='Ano').merge(maior_salario, on='Ano')
analise_salarial.columns = ['Ano', 'Emprego Formal', 'Massa de Rendimentos', 'Média Salarial', 'Menor Salário', 'Maior Salário']

# Formatar os valores para exibição
analise_salarial['Massa de Rendimentos'] = analise_salarial['Massa de Rendimentos'].apply(lambda x: f'{x:,.2f}')
analise_salarial['Média Salarial'] = analise_salarial['Média Salarial'].apply(lambda x: f'{x:,.2f}')
analise_salarial['Menor Salário'] = analise_salarial['Menor Salário'].apply(lambda x: f'{x:,.2f}')
analise_salarial['Maior Salário'] = analise_salarial['Maior Salário'].apply(lambda x: f'{x:,.2f}')

print(analise_salarial)

analise_salarial.to_csv('./src/data/tratado/raisbdanalisesalarial.csv',sep=';',index=False)