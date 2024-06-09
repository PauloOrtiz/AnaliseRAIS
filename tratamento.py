import pandas as pd 

RaisBD = pd.read_csv('./src/data/raisbd.csv',sep=';',encoding='latin1',index_col=False)




RaisBDcountnull = RaisBD.isnull().sum()

RaisBDnull = RaisBD[RaisBD.isnull().any(axis=1)]


RaisBDcountnull.to_csv('./src/data/tratado/raisbdcountnull.csv',sep=';')
RaisBDnull.to_csv('./src/data/tratado/raisbdnull.csv',sep=';', index= False)


print(RaisBD.shape)

RaisBD = RaisBD.dropna()

print(RaisBD.shape)