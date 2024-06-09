import streamlit as st
import pandas as pd

st.set_page_config(page_title="Coleta e Tratamento de Dados RAIS")

st.title("Coleta e Tratamento de Dados RAIS - São Paulo")

with open("./src/css/style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Coleta", "Tratamento"])

with tab1:
    st.markdown( """
                
    ## Introdução

    Bem-vindo à nossa página dedicada à coleta e tratamento de dados do Relatório Anual de Informações Sociais (RAIS) especificamente para o estado de São Paulo.

    ## Importância do RAIS

    O RAIS é uma ferramenta essencial para a coleta de dados sobre o mercado de trabalho formal no Brasil. Ele foi instituído para atender às necessidades de controle da atividade trabalhista e fornecer informações detalhadas ao governo sobre o mercado de trabalho. Esses dados são fundamentais para a formulação de políticas públicas, pesquisas acadêmicas e planejamento empresarial.

    ## Coleta dos Dados

    Os dados do RAIS para o estado de São Paulo estão disponíveis no [Repositório SEADE](https://repositorio.seade.gov.br/dataset/emprego-rais-e-arquivos-auxiliares). Esses arquivos abrangem informações detalhadas de emprego de diversos anos, permitindo uma análise profunda e abrangente das tendências e dinâmicas do mercado de trabalho.

    ## Disponibilidade dos Dados

    Os dados do RAIS para São Paulo estão disponíveis para os anos de 2012 a 2021. Cada ano traz um conjunto rico de informações que inclui, entre outros:
    - Número de empregados
    - Remuneração
    - Grau de instrução
    - Ocupação
    - Setor de atividade econômica

    ## Trabalhando com os Dados

    Nos próximos passos, iremos nos aprofundar no tratamento desses dados. Aqui está um breve resumo do que faremos:
    1. **Coleta dos Arquivos**: Baixaremos os arquivos de dados do Repositório SEADE.
    2. **Carregamento dos Dados**: Usaremos ferramentas como pandas para carregar os dados em nossos ambientes de análise.
    3. **Tratamento dos Dados**: Realizaremos o pré-processamento necessário, como a limpeza dos dados e a filtragem para o estado de São Paulo.
    4. **Análise Exploratória**: Executaremos análises exploratórias para entender as tendências e padrões nos dados.
    5. **Visualização dos Dados**: Criaremos visualizações interativas para apresentar os insights de maneira clara e informativa.

    ## Conclusão

    Este processo de coleta e tratamento dos dados do RAIS é fundamental para entender melhor o mercado de trabalho em São Paulo. Com essas informações, podemos tomar decisões mais informadas, criar políticas públicas mais eficazes e contribuir para o desenvolvimento econômico e social do estado.

    """)

with tab2:
    # Carregar os dados
    DBhead2012a2020 = pd.read_csv('./src/data/tratado/rais2012a2020head.csv', sep=';', encoding='ISO-8859-1', index_col=False)
    DBinfo2012a2020 = pd.read_csv('./src/data/tratado/rais2012a2020info.csv', sep=';', encoding='ISO-8859-1', index_col=False)
    DBhead2021 = pd.read_csv('./src/data/tratado/rais2021head.csv', sep=';', encoding='ISO-8859-1', index_col=False)
    DBinfo2021 = pd.read_csv('./src/data/tratado/rais2021info.csv', sep=';', encoding='ISO-8859-1', index_col=False)
    DBraisdbcountnull = pd.read_csv('./src/data/tratado/raisbdcountnull.csv', sep=';', encoding='ISO-8859-1')
    DBraisdbnull = pd.read_csv('./src/data/tratado/raisbdnull.csv', sep=';', encoding='ISO-8859-1', index_col=False)

    # Markdown para o cabeçalho e descrição
    st.markdown("""
    # Análise dos Conjuntos de Dados RAIS

    ## Dados Disponíveis:

    O governo do Estado de São Paulo disponibiliza dois conjuntos de dados sobre a RAIS: um abrangendo os anos de 2012 a 2020, e outro contendo dados de 2021. Vamos explorar esses dados para entender melhor o seu conteúdo e estrutura.

    ### RAIS 2012 a 2020
    """)
    st.dataframe(DBhead2012a2020, hide_index=True)
    st.dataframe(DBinfo2012a2020, hide_index=True)

    st.markdown("### RAIS 2021")
    st.dataframe(DBhead2021, hide_index=True)
    st.dataframe(DBinfo2021, hide_index=True)

    st.markdown("""
    ## Comparação e Tratamento dos Dados

    Ao examinar os dois conjuntos de dados, percebemos que, embora contenham informações comuns, há colunas distintas em cada um. Para nossa análise, decidimos excluir as colunas 'Categoria de estabelecimento', 'fator de correção_2012_2021' e 'Ordena_TAMESTB'.

    Além disso, ajustamos o tipo de algumas colunas. Por exemplo, a coluna 'Cod_IBGE', que estava como float, foi alterada para string, pois não realizaremos cálculos com ela. Também modificamos a coluna 'Ano' no conjunto de dados de 2021 para string, mantendo apenas o ano, já que a declaração é anual.

    ### Tratamento dos Dados
    Abaixo está o código utilizado para o tratamento dos dados:
    """)

    with st.expander('Código de Tratamento'):
        st.code('''
import pandas as pd 

# Carregar os dados
rais2021 = pd.read_csv('./src/data/rais2021.csv', sep=';', encoding='latin1')
rais2012a2020 = pd.read_csv('./src/data/Rais_painel.csv', sep=';', encoding='ISO-8859-1')

# Tratamento do Rais2012a2020
rais2012a2020.rename(columns={'ï»¿ANO': 'Ano'}, inplace=True)
rais2012a2020 = rais2012a2020.drop(columns=['Escolaridade'])
rais2012a2020['massa_rendimentos'] = rais2012a2020['massa_rendimentos'].str.replace(',', '.').astype(float)
rais2012a2020 = rais2012a2020.astype({'Ano': 'str', 'Cod_ibge': 'str', 'CLAS_CNAE_20': 'str', 'GR_INSTRUCAO': 'str', 'TAMESTAB': 'str'})

# Tratamento do Rais2021
rais2021 = rais2021.drop(columns=['fator de correÃ§Ã£o_2012_2021', 'Ordena_TAMESTB', 'Categoria de estabelecimento', 'Escolaridade'])
rais2021['Ano'] = pd.to_datetime(rais2021['Ano'])
rais2021['Ano'] = rais2021['Ano'].dt.year
rais2021['massa_rendimentos'] = rais2021['massa_rendimentos'].str.replace(',', '.').astype(float)
rais2021 = rais2021.astype({'Cod_ibge': 'str', 'CBO2002_FAMILIA': 'str', 'CLAS_CNAE_20': 'str', 'GR_INSTRUCAO': 'str', 'TAMESTAB': 'str', 'Ano': 'str'})
rais2021 = rais2021.dropna()

# Combinar os conjuntos de dados
RaisBD = pd.concat([rais2012a2020, rais2021], ignore_index=True)

# Salvar o DataFrame combinado
RaisBD.to_csv('./src/data/raisBD.csv', sep=';', index=False)
        ''', language='python')

    st.markdown("""
    ## Dados Nulos

    Durante o tratamento dos dados, identificamos 10 registros com o código IBGE nulo no conjunto de dados de 2021. Como essa quantidade é pequena, optamos por excluir esses registros.

    Abaixo estão as informações sobre a contagem de valores nulos por coluna:
    """)
    st.dataframe(DBraisdbcountnull, hide_index=True)

    st.markdown("""
    Aqui estão os registros com valores nulos:
    """)
    st.dataframe(DBraisdbnull, hide_index=True)

    st.markdown("""
    ## Conclusão

    Após o tratamento, combinamos os dados em um único DataFrame contendo 25.823.502 registros e 9 colunas. Na próxima página, começaremos com as análises iniciais. Venha acompanhar!
    """)