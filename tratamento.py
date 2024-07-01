import pandas as pd 

RaisBD = pd.read_csv('./src/data/raisbd.csv',sep=';',encoding='latin1',index_col=False)
CneaBD = pd.read_excel('./src/data/cnae_20.xlsx',dtype={'Cod_Classe': str})

RaisBD['CLAS_CNAE_20'] = RaisBD['CLAS_CNAE_20'].astype(str)
CneaBD['Cod_Classe'] = CneaBD['Cod_Classe'].astype(str)

result= pd.merge(RaisBD, CneaBD, left_on='CLAS_CNAE_20', right_on='Cod_Classe')

def get_top_cnaes(df, setor, top_n=10, order='desc'):
    df_setor = df[df['SETOR'] == setor]
    if order == 'desc':
        return df_setor.groupby(['Ano', 'CLAS_CNAE_20', 'Descr_Classe'])['Emprego_formal'].sum().reset_index().sort_values(by='Emprego_formal', ascending=False).groupby('Ano').head(top_n)
    else:
        return df_setor.groupby(['Ano', 'CLAS_CNAE_20', 'Descr_Classe'])['Emprego_formal'].sum().reset_index().sort_values(by='Emprego_formal').groupby('Ano').head(top_n)

top10_industria = get_top_cnaes(result, 'Indústria', top_n=10, order='desc')

#print(top10_industria.head(100))




top10_industria.to_csv('./src/data/tratado/Raistop10descindustriageral.csv', sep=';', index=False)