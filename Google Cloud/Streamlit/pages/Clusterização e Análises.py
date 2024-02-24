import streamlit as st
import io
import pandas as pd
import plotly.graph_objects as go
from google.cloud import storage
from googleapiclient.discovery import build
from google.oauth2 import service_account


# Configurando a página do Streamlit
st.set_page_config(page_title='Análise e Grupos',
                   page_icon='🛍️',
                   layout='wide')

# Carrega as credenciais da conta de serviço
creds = service_account.Credentials.from_service_account_file('C:/path/to/your/service-account-file.json')

# Função para carregar o modelo - não é mais necessária, pois estamos usando o Vertex AI
@st.cache_resource
def carregar_modelo():
    pass

# Função para enviar dados para o endpoint do Vertex AI
def enviar_dados_para_endpoint(dados):
    # Construindo o serviço do Vertex AI
    ai_service = build('aiplatform', 'v1', credentials=creds)

    # Definindo o nome do endpoint
    endpoint = 'projects/PROJECT_ID/locations/us-central1/endpoints/kmeansmeli-endpoint'

    # Formatando os dados para a solicitação
    instances = dados.values.tolist()

    # Criando a solicitação
    request = ai_service.projects().locations().endpoints().predict(
        endpoint=endpoint,
        body={
            'instances': instances
        }
    )

    # Enviando a solicitação e obtendo a resposta
    response = request.execute()

    # Retornando os rótulos dos clusters
    return [item['clusterIndex'] for item in response['predictions']]

# Função para carregar dados do Google Cloud Storage
def carregar_dados_gcs(bucket_name, file_name):
    # Criando um cliente de armazenamento
    storage_client = storage.Client()

    # Obtendo o bucket
    bucket = storage_client.get_bucket(bucket_name)

    # Obtendo o blob
    blob = bucket.blob(file_name)

    # Baixando o blob como uma string
    data_string = blob.download_as_text()

    # Carregando os dados como um DataFrame
    dados = pd.read_json(io.StringIO(data_string))

    return dados

# Função para plotar gráficos
def plotar_graficos(df):
    # Agrupando os dados por Grupo e calculando a mediana do Preço
    df_median = df.groupby('Grupo')['Preço'].median().reset_index()

    # Criando um gráfico de barras interativo com a mediana do preço por Grupo
    fig = go.Figure()

    for i, grupo in enumerate(df_median['Grupo']):
        fig.add_trace(go.Bar(
            x=[grupo],
            y=[df_median.loc[i, 'Preço']],
            text=df_median.loc[i, 'Preço'],
            textposition='auto',
            name=grupo
        ))

    # Atualizando o layout do gráfico para incluir a legenda interativa
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'},
                      hovermode="x", title="Mediana de Preço por Grupo")

    st.plotly_chart(fig)

# Sidebar
opcao = st.sidebar.selectbox('Escolha uma opção', ['Grupos', 'Trends'])

if opcao == 'Grupos':
    # Carregando os dados do Google Cloud Storage
    dados = carregar_dados_gcs('itens-meli', 'dados.json')

    # Novos dados
    X = dados[['Preço', 'Visitas', 'Estrelas']]

    # Obtendo os rótulos dos clusters para os novos dados
    labels = enviar_dados_para_endpoint(X)

    # Adicionando os rótulos dos clusters ao DataFrame de dados
    dados['Cluster'] = labels

    # Definindo um dicionário que mapeia os rótulos dos clusters para os nomes dos grupos
    cluster_names = {
    0: "Desconhecidos baratos",
    1: "Aclamados",
    2: "Baratos de qualidade variada"
}

    # Adicionando uma nova coluna 'Grupo' ao DataFrame que mapeia os rótulos dos clusters para os nomes dos grupos
    dados['Grupo'] = dados['Cluster'].map(cluster_names)

    # Gráficos
    plotar_graficos(dados)

    # Criando um widget de seleção para escolher um grupo
    grupos = dados['Grupo'].dropna().unique()
    grupo_selecionado = st.selectbox('Escolha um grupo', grupos)

    # Filtrando o DataFrame para incluir apenas os itens do grupo selecionado
    dados_filtrados = dados[dados['Grupo'] == grupo_selecionado]

    # Transformando a coluna 'Link' em uma coluna de links clicáveis
    dados_filtrados['Link'] = dados_filtrados['Link'].apply(lambda x: f'<a href="{x}">Link</a>')

    # Removendo as colunas especificadas
    dados_filtrados = dados_filtrados.drop(columns=['ID do produto','Categoria','Cluster','Grupo']).reset_index(drop=True)

    # Criando um widget de seleção para escolher uma marca
    marcas = dados_filtrados['Marca'].unique().tolist()
    marcas.insert(0, 'Todas')
    marca_selecionada = st.selectbox('Escolha uma marca', marcas)

    if marca_selecionada != 'Todas':
        dados_filtrados = dados_filtrados[dados_filtrados['Marca'] == marca_selecionada]

    # Criando um widget de controle deslizante para escolher um intervalo de preços
    preco_min = int(dados_filtrados['Preço'].min())
    preco_max = int(dados_filtrados['Preço'].max())

    if preco_min < preco_max:
        preco_range = st.slider('Escolha um intervalo de preços', min_value=preco_min, max_value=preco_max, value=(preco_min, preco_max))
        dados_filtrados = dados_filtrados[(dados_filtrados['Preço'] >= preco_range[0]) & (dados_filtrados['Preço'] <= preco_range[1])]

    # Mostrando o DataFrame filtrado
    st.write(dados_filtrados.to_html(index=False,escape=False), unsafe_allow_html=True)

else:
    # Carregando os dados das tendências do Google Cloud Storage
    trends = carregar_dados_gcs('itens-meli', 'tendencias.json')

    # Exibindo as tendências de forma apresentável
    for trend in trends:
        st.markdown(f"* {trend}")