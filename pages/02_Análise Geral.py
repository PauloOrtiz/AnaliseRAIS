import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64



st.set_page_config(page_title="Coleta e Tratamento de Dados RAIS", layout='wide')

st.title("Analisando os Dados RAIS - São Paulo")

with open("./src/css/style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
tab1, tab2,tab3, tab4 = st.tabs(["Empregos formais", "Salário","Setores Produtivos", "CNEA"])


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
            text='Quantidade de Empregos Formais por Ano',
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

    st.markdown("""
    ## Resultados da Análise
    ### Média Salarial
    O gráfico abaixo mostra a evolução da média salarial no estado de São Paulo ao longo dos anos.


    ### Menor Salário
    O gráfico abaixo mostra a variação do menor salário ao longo dos anos, considerando apenas empresas com um único funcionário.


    ### Maior Salário
    O gráfico abaixo ilustra a evolução do maior salário no estado de São Paulo, refletindo possíveis picos em setores específicos.


    ### Observações
    **Média Salarial**: A média salarial apresenta uma tendência de crescimento ao longo dos anos, indicando um aumento geral nos rendimentos dos empregados formais no estado de São Paulo.

    **Menor Salário**: O menor salário, ao considerarmos apenas empresas com um único funcionário, mostrou variações menores ao longo dos anos, mas ainda assim um aumento gradual, refletindo possíveis ajustes salariais mínimos.

    **Maior Salário**: O maior salário mostra variações mais significativas, possivelmente refletindo rendimentos excepcionais em alguns anos específicos.

    ###Conclusão
    A análise descritiva dos salários no estado de São Paulo revela uma tendência de aumento nos rendimentos médios dos empregados formais ao longo dos anos. Enquanto o menor salário aumentou de forma mais estável, o maior salário variou mais significativamente, refletindo aumentos em setores específicos ou posições de alto rendimento.
    """)

with tab3:
    SetorgeralRaiS = pd.read_csv('./src/data/tratado/Raisempregoporsetor.csv', sep=';', index_col=False)

    st.markdown("""
        ## Análise Geral dos Empregos Formais por Setor

        ### Introdução ao CNAE

        A **Classificação Nacional de Atividades Econômicas (CNAE)** é um sistema utilizado pelo governo brasileiro para categorizar e organizar as atividades econômicas no país. Essa classificação é essencial para a análise econômica, pois permite agrupar e comparar dados de diferentes setores de forma padronizada.

        ### Os Três Grandes Grupos de Setores

        A CNAE divide todas as atividades econômicas em três grandes grupos principais:

        - **Agricultura**: Inclui atividades relacionadas ao cultivo de plantas, criação de animais, produção florestal e pesca.
        - **Indústria**: Abrange as atividades de transformação de bens e produtos, incluindo a manufatura, construção e outras atividades industriais.
        - **Serviços**: Envolve uma ampla gama de atividades que não produzem bens tangíveis, como comércio, transporte, educação, saúde e serviços financeiros.

        ## Primeira Análise

        Nesta primeira etapa da nossa análise, vamos focar na distribuição de empregos formais entre esses três grandes grupos. Entender como os empregos são distribuídos entre Agricultura, Indústria e Serviços nos dará uma visão geral da estrutura econômica do estado de São Paulo.

    """)

    fig_setor = go.Figure()


    setores = SetorgeralRaiS['SETOR'].unique()
    for setor in setores:
        setor_data = SetorgeralRaiS[SetorgeralRaiS['SETOR'] == setor]
        fig_setor.add_trace(
            go.Scatter(
                x=setor_data['Ano'],
                y=setor_data['Emprego_formal'],
                mode='lines+markers',
                name=setor,
                text=setor_data['SETOR'],
                hovertemplate='<b>%{x}</b><br>Emprego Formal: %{y}<br>Setor: %{text}<extra></extra>'
            )
        )

    # Configurar layout do gráfico
    fig_setor.update_layout(
        title=dict(
            text='Emprego Formal por Setor ao Longo dos Anos',
            font=dict(family='Arial, sans-serif', size=24, color='#CD8D00'),
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
            title='Emprego Formal',
            titlefont=dict(size=16, color='#004175'),
            gridcolor='lightgray',        
        ),
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig_setor)
                
    st.markdown("""
                
    ## Análise Descritiva dos Empregos Formais por Setor no Estado de São Paulo

    Conforme podemos observar no gráfico acima, o estado de São Paulo apresenta uma distribuição significativa de empregos formais no setor de **Serviços**, seguido pela **Indústria** e **Agropecuária**. Essa distribuição reflete a estrutura econômica do estado, que é o maior centro econômico do Brasil.

    ### Setor de Serviços

    O setor de serviços é o maior empregador formal em São Paulo, com uma média de mais de 10 milhões de empregos formais ao longo dos anos. Esse setor inclui uma vasta gama de atividades, como comércio, transporte, educação, saúde e serviços financeiros. A predominância do setor de serviços pode ser atribuída ao fato de São Paulo ser a capital financeira do país, abrigando as sedes das principais empresas e instituições financeiras, bem como uma infraestrutura robusta de comércio e serviços.

    ### Setor Industrial

    A indústria, embora menor que o setor de serviços, ainda desempenha um papel crucial na economia paulista, com aproximadamente 3 milhões de empregos formais em média. A presença de grandes polos industriais e parques tecnológicos em cidades como São Bernardo do Campo, Campinas e Sorocaba contribui significativamente para esses números. A indústria paulista é diversificada, abrangendo manufatura, construção civil, automotiva e muitas outras subáreas.

    ### Setor Agropecuário

    O setor agropecuário, apesar de ser o menor dos três em termos de emprego formal, continua sendo essencial para a economia do estado, especialmente nas regiões interioranas. Com uma média de cerca de 300 mil empregos formais, esse setor inclui atividades agrícolas, pecuárias e florestais. A produção agropecuária de São Paulo é diversificada e inclui cana-de-açúcar, laranja, café e carne bovina, produtos que são importantes tanto para o mercado interno quanto para a exportação.

    ### Tendências ao Longo dos Anos

    - **Serviços**: O setor de serviços mostrou um crescimento constante, com um leve declínio em 2016, possivelmente devido à crise econômica, seguido por uma recuperação sólida até 2021.
    - **Indústria**: A indústria sofreu uma queda significativa entre 2014 e 2017, refletindo as dificuldades econômicas enfrentadas pelo país, mas começou a mostrar sinais de recuperação nos anos subsequentes.
    - **Agropecuária**: A agropecuária manteve-se relativamente estável ao longo dos anos, com pequenas flutuações que refletem as safras anuais e mudanças climáticas.

    ### Conclusão

    A análise dos empregos formais nos setores de Agropecuária, Indústria e Serviços no estado de São Paulo revela uma economia diversificada e resiliente. O setor de serviços destaca-se como o pilar do mercado de trabalho formal, refletindo a importância da capital paulista como centro econômico e financeiro do Brasil. A indústria, apesar dos desafios, continua sendo uma força significativa, enquanto a agropecuária mantém sua relevância, especialmente nas regiões interioranas.

    Essa análise fornece uma visão geral crucial para entender a estrutura econômica de São Paulo. No próximo passo, exploraremos em mais detalhes os fatores que impulsionam essas tendências e como podemos usar essas informações para fomentar um desenvolvimento econômico sustentável e inclusivo.

    ### Dados e Metodologia

    Utilizamos dados fornecidos pelo governo, especificamente a tabela do CNAE, para categorizar os empregos formais de acordo com esses três grandes grupos. A partir dessa categorização, podemos observar como cada grupo contribui para o mercado de trabalho formal.

    """)

with tab4:


    
    file_ = open(".\src\img\gif\Top10Empregoporsetor.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
        unsafe_allow_html=True,
    )

    top10descindustria = pd.read_csv('./src/data/tratado/Raistop10descindustriageral.csv',sep=';',index_col=False)
    top10descindustria = top10descindustria.sort_values(by=['Ano'])

    fig_top10 = go.Figure()

       
    setores = top10descindustria['Descr_Classe'].unique()
    for setor in setores:
        setor_data = top10descindustria[top10descindustria['Descr_Classe'] == setor]
        fig_top10.add_trace(
            go.Scatter(
                x=setor_data['Ano'],
                y=setor_data['Emprego_formal'],
                mode='lines+markers',
                name=setor,
                text=setor_data['Descr_Classe'],
                hovertemplate='<b>%{x}</b><br>Emprego Formal: %{y}<br>Setor: %{text}<extra></extra>'
            )
        )

    # Configurar layout do gráfico
    fig_top10.update_layout(
        title=dict(
            text='Emprego Formal por Setor ao Longo dos Anos',
            font=dict(family='Arial, sans-serif', size=24, color='#CD8D00'),
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
            title='Emprego Formal',
            titlefont=dict(size=16, color='#004175'),
            gridcolor='lightgray',        
        ),
    )

    st.plotly_chart(fig_top10)