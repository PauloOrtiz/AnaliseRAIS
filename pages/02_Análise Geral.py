import streamlit as st
import pandas as pd
import plotly.graph_objects as go


st.set_page_config(page_title="Coleta e Tratamento de Dados RAIS")

st.title("Analisando os Dados RAIS - São Paulo")

with open("./src/css/style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
tab1, tab2 = st.tabs(["Empregos formais", "Salário"])


with tab1:
    st.markdown("""

        ## Explorando os dados:

        Conforme a metodologia aplicada, localizada no [link](https://repositorio.seade.gov.br/dataset/a6a99b6a-9339-476e-9d88-38bf5b4ff034/resource/5fe8c1fd-c338-45b0-bf31-39b81a411245/download/emprego_salario_metodologia.pdf), o registro dos dados no banco de dados da RAIS é composto por uma combinação de fatores:

        - **Empresa**
        - **Cidade**
        - **CNAE**
        - **Grau de escolaridade**

        Isso significa que uma empresa que emprega pessoas com vários níveis de escolaridade pode ter vários registros dentro do banco de dados. Desta forma, não é correto olhar apenas para a quantidade de registros por ano para determinar se houve um aumento de emprego em um ano ou não. 

        Para visualizar corretamente, utilizaremos a coluna de emprego formal. Abaixo, podemos ver o gráfico que mostra a quantidade de empregos formais no estado de São Paulo, segundo a RAIS, entre 2012 e 2021.
    """)
    RaisBDano = pd.read_csv('./src/data/tratado/Qntraisbdempregoporano.csv', sep=';', index_col=False)
    RaisBDano['Quantidade de emprego formatada'] = RaisBDano['Quantidade de emprego'].apply(lambda x: f"{x:,}")

    fig_ano = go.Figure()
    fig_ano.add_trace(
        go.Scatter(
            x=RaisBDano['Ano'],
            y=RaisBDano['Quantidade de emprego'],
            mode='lines+markers+text',
            text=RaisBDano['Quantidade de emprego formatada'],
            textposition='bottom center',
            textfont=dict(
                family='Arial, sans-serif',
                size=14,
                color='darkblue'
            ),
            marker=dict(
                color='blue',
                size=7,
                symbol='circle'
            )
        )
    )
    fig_ano.update_layout(
        title=dict(
            text='Quantidade de Registros por Ano',
            font=dict(
                family='Arial, sans-serif',
                size=24,
                color= '#CD8D00'
            ),
            x=0.5,  # Centralizado horizontalmente
            y=0.9,  # Perto do topo
            xanchor='center',
            yanchor='top'
        ),
        xaxis=dict(
            title='Ano',
            titlefont=dict(size=16, color='#004175'),
            gridcolor='lightgray',        
            showline=True,        
            mirror=True,
            tickangle=45,
            tickformat='%Y',  
        ),
        yaxis=dict(
            title='Quantidade de Registro',
            titlefont=dict(size=16, color='#004175'),
            gridcolor='lightgray',        
        ),
    )

    st.plotly_chart(fig_ano)

    st.markdown("""

        ### Observações:

        1. **Crescimento Inicial**: Observa-se um crescimento constante no número de empregos formais de 2012 até 2014. Em 2014, o número de empregos formais atingiu o pico de 14.111.450.

        2. **Declínio Durante a Crise**: A partir de 2015, houve uma queda significativa no número de empregos formais, coincidindo com a crise econômica que afetou o Brasil. O número de empregos formais caiu para 13.194.120 em 2016.

        3. **Estabilização e Recuperação**: Após o declínio, o mercado de trabalho formal começou a estabilizar e mostrar sinais de recuperação. De 2017 a 2019, o número de empregos formais aumentou gradualmente.

        4. **Impacto da Pandemia**: Em 2020, houve uma leve queda no número de empregos formais devido ao impacto da pandemia de COVID-19, mas o número voltou a subir em 2021, alcançando 13.848.390 empregos formais.
    """)

with tab2:

    RaisBDSalario = pd.read_csv('./src/data/tratado/raisbdanalisesalarial.csv', sep=';', index_col=False)

    st.markdown(""" 
    ## Análise Descritiva Salarial

    Vamos falar sobre a coluna de `massa_rendimentos`, que representa os salários mensais somados de todos os empregados de um determinado mês. Para obter uma análise precisa, precisamos considerar alguns fatores importantes e filtrar certos registros:

    1. **Salários Zerados**: Desconsideramos registros onde o resultado da divisão entre `massa_rendimentos` e `emprego_formal` é zero. Isso ocorre geralmente em empresas com um único funcionário (normalmente o dono), que pode não receber um salário formal.

    2. **Registros Inválidos**: Para evitar distorções, também filtramos empresas com múltiplos funcionários ganhando valores irreais. Consideramos apenas empresas com um único funcionário para calcular o menor salário aceitável, pois encontramos salários mínimos extremamente baixos, em torno de 9 reais.
    """)

    with st.expander('Código de Tratamento dos Dados'):
        st.code(body=
            """import pandas as pd 

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



        analise_salarial.to_csv('./src/data/tratado/raisbdanalisesalarial.csv',sep=';',index=False)")
    """,language='python')
    
    fig_media = go.Figure()
    fig_media.add_trace(
        go.Scatter(
            x=RaisBDSalario['Ano'],
            y=RaisBDSalario['Média Salarial'],
            mode='lines+markers+text',
            text=RaisBDSalario['Média Salarial'],
            textposition='top center',
            textfont=dict(
                family='Arial, sans-serif',
                size=14,
                color='darkblue'
            ),
            marker=dict(
                color='blue',
                size=7,
                symbol='circle'
            )
        )
    )
    fig_media.update_layout(
        title=dict(
            text='Média Salarial por Ano',
            font=dict(
                family='Arial, sans-serif',
                size=24,
                color= '#CD8D00'
            ),
            x=0.5,  # Centralizado horizontalmente
            y=0.9,  # Perto do topo
            xanchor='center',
            yanchor='top'
        ),
        xaxis=dict(
            title='Ano',
            titlefont=dict(size=16, color='#004175'),
            gridcolor='lightgray',        
            showline=True,        
            mirror=True,
            tickangle=45,
            tickformat='%Y',  
        ),
        yaxis=dict(
            title='Valores em R$',
            titlefont=dict(size=16, color='#004175'),
            gridcolor='lightgray',        
        ),
    )

    st.plotly_chart(fig_media)

    fig_maior = go.Figure()
    fig_maior.add_trace(
        go.Scatter(
            x=RaisBDSalario['Ano'],
            y=RaisBDSalario['Maior Salário'],
            mode='lines+markers+text',
            text=RaisBDSalario['Maior Salário'],
            textposition='top center',
            textfont=dict(
                family='Arial, sans-serif',
                size=14,
                color='darkblue'
            ),
            marker=dict(
                color='blue',
                size=7,
                symbol='circle'
            )
        )
    )
    fig_maior.update_layout(
        title=dict(
            text='Maior Salário por Ano',
            font=dict(
                family='Arial, sans-serif',
                size=24,
                color= '#CD8D00'
            ),
            x=0.5,  # Centralizado horizontalmente
            y=0.9,  # Perto do topo
            xanchor='center',
            yanchor='top'
        ),
        xaxis=dict(
            title='Ano',
            titlefont=dict(size=16, color='#004175'),
            gridcolor='lightgray',        
            showline=True,        
            mirror=True,
            tickangle=45,
            tickformat='%Y',  
        ),
        yaxis=dict(
            title='Valores em R$',
            titlefont=dict(size=16, color='#004175'),
            gridcolor='lightgray',        
        ),
    )

    st.plotly_chart(fig_maior)

    fig_menor = go.Figure()
    fig_menor.add_trace(
        go.Scatter(
            x=RaisBDSalario['Ano'],
            y=RaisBDSalario['Menor Salário'],
            mode='lines+markers+text',
            text=RaisBDSalario['Menor Salário'],
            textposition='top center',
            textfont=dict(
                family='Arial, sans-serif',
                size=14,
                color='darkblue'
            ),
            marker=dict(
                color='blue',
                size=7,
                symbol='circle'
            )
        )
    )
    fig_menor.update_layout(
        title=dict(
            text='Menor Salário por Ano',
            font=dict(
                family='Arial, sans-serif',
                size=24,
                color= '#CD8D00'
            ),
            x=0.5,  # Centralizado horizontalmente
            y=0.9,  # Perto do topo
            xanchor='center',
            yanchor='top'
        ),
        xaxis=dict(
            title='Ano',
            titlefont=dict(size=16, color='#004175'),
            gridcolor='lightgray',        
            showline=True,        
            mirror=True,
            tickangle=45,
            tickformat='%Y',  
        ),
        yaxis=dict(
            title='Valores em R$',
            titlefont=dict(size=16, color='#004175'),
            gridcolor='lightgray',        
        ),
    )

    st.plotly_chart(fig_menor)

      