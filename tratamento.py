import pandas as pd 

RaisBD = pd.read_csv('./src/data/raisbd.csv',sep=';',encoding='latin1',index_col=False)
CneaBD = pd.read_excel('./src/data/cnae_20.xlsx',dtype={'Cod_Classe': str})

RaisBD['CLAS_CNAE_20'] = RaisBD['CLAS_CNAE_20'].astype(str)
CneaBD['Cod_Classe'] = CneaBD['Cod_Classe'].astype(str)

result= pd.merge(RaisBD, CneaBD, left_on='CLAS_CNAE_20', right_on='Cod_Classe')

result = result.groupby(['Ano', 'SETOR'])['Emprego_formal'].sum().reset_index()

result = result.sort_values(by=['Ano', 'SETOR'])


result.to_csv('./src/data/tratado/Raisempregoporsetor.csv', sep=';', index=False)