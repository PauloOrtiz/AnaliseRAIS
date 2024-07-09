import pandas as pd 
import bar_chart_race as bcr


RaisBD = pd.read_csv('./src/data/raisbd.csv', sep=';', encoding='latin1', dtype={'CLAS_CNAE_20': str})
CneaBD = pd.read_excel('./src/data/cnae_20.xlsx', dtype={'Cod_Classe': str})


RaisBD['CLAS_CNAE_20'] = RaisBD['CLAS_CNAE_20'].astype(str)
CneaBD['Cod_Classe'] = CneaBD['Cod_Classe'].astype(str)


result = pd.merge(RaisBD, CneaBD, left_on='CLAS_CNAE_20', right_on='Cod_Classe')


result['Emprego_formal'] = pd.to_numeric(result['Emprego_formal'], errors='coerce')

def get_top_cnaes(df, setor, top_n=10, order='desc'):
    df_setor = df[df['SETOR'] == setor]
    if order == 'desc':
        return df_setor.groupby(['Ano', 'CLAS_CNAE_20', 'Descr_Classe'])['Emprego_formal'].sum().reset_index().sort_values(by='Emprego_formal', ascending=False).groupby('Ano').head(top_n)
    else:
        return df_setor.groupby(['Ano', 'CLAS_CNAE_20', 'Descr_Classe'])['Emprego_formal'].sum().reset_index().sort_values(by='Emprego_formal').groupby('Ano').head(top_n)

def create_bar_chart_race(df_pivot, filename, setor):
    """
    Cria e salva a animação do gráfico de barras.
    """
    bcr.bar_chart_race(
        df=df_pivot.pivot(index='Ano', columns='Descr_Classe', values='Emprego_formal').fillna(0),
        filename=filename,
        orientation='h',
        sort='desc',
        n_bars=10,
        fixed_order=False,
        fixed_max=True,
        steps_per_period=10,
        interpolate_period=False,
        label_bars=True,
        bar_size=.95,
        period_label={'x': .99, 'y': .25, 'ha': 'right', 'va': 'center'},
        period_fmt='{x:.0f}',
        period_summary_func=lambda v, r: {'x': .99, 'y': .18, 
                                          's': f'Total Empregos: {v.sum():,.0f}', 
                                          'ha': 'right', 'size': 8, 'family': 'Courier New'},
        perpendicular_bar_func='median',
        period_length=2000,
        figsize=(10, 6),
        dpi=144,
        cmap='dark12',
        title=f'Evolução do Emprego Formal no Setor {setor}',
        title_size=16,
        bar_label_size=7,
        tick_label_size=7,
        shared_fontdict={'family': 'Arial', 'color': '.1'},
        scale='linear',
        writer=None,
        fig=None,
        bar_kwargs={'alpha': .7},
        filter_column_colors=False
    )

top10_industria_desc = get_top_cnaes(result, 'Indústria', top_n=10, order='desc')
top10_industria_asc = get_top_cnaes(result, 'Indústria', top_n=10, order='asc')
top10_servico_desc = get_top_cnaes(result, 'Serviços', top_n=10, order='desc')
top10_servico_asc = get_top_cnaes(result, 'Serviços', top_n=10, order='asc')
top10_agropecuaria_desc = get_top_cnaes(result, 'Agropecuária', top_n=10, order='desc')
top10_agropecuaria_asc = get_top_cnaes(result, 'Agropecuária', top_n=10, order='asc')



top10_agropecuaria_asc.to_csv('./src/data/tratado/Raistop10ascagropecuariageral.csv',sep=';',index=False)
top10_agropecuaria_desc.to_csv('./src/data/tratado/Raistop10descagropecuariageral.csv',sep=';',index=False)
top10_industria_asc.to_csv('./src/data/tratado/Raistop10ascindustriageral.csv',sep=';',index=False)
top10_industria_desc.to_csv('./src/data/tratado/Raistop10descindustriageral.csv',sep=';',index=False)
top10_servico_asc.to_csv('./src/data/tratado/Raistop10ascservicogeral.csv',sep=';',index=False)
top10_servico_desc.to_csv('./src/data/tratado/Raistop10descservicogeral.csv',sep=';',index=False)


