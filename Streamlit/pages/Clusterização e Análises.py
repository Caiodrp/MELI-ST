import streamlit as st
import requests
import joblib
import os 
import json
import io
import pandas as pd
import plotly.graph_objects as go
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Definir o template
st.set_page_config(page_title='Análise e Grupos',
                   page_icon='🛍️',
                   layout='wide')

# Função para carregar o modelo
@st.cache_resource
def carregar_modelo():
    url = 'https://github.com/Caiodrp/MELI-ST/raw/main/kmeans_meli.joblib'
    response = requests.get(url)
    modelo = joblib.load(io.BytesIO(response.content))
    return modelo

def obter_ids_arquivos():
    # Carrega as credenciais da variável de ambiente
    creds_json = os.environ.get('CRED_SERVICE_ACCOUNT')
    creds = service_account.Credentials.from_service_account_info(json.loads(creds_json))

    # Constrói o serviço
    drive_service = build('drive', 'v3', credentials=creds)

    # ID da pasta principal
    main_folder_id = '1qOQ4kcd2MnEprD17dqFAQyOGT9zfYgoa'

    # Obtém a lista de subpastas (categorias) na pasta principal
    results = drive_service.files().list(
        q=f"'{main_folder_id}' in parents",
        fields="nextPageToken, files(id, name, mimeType)"
    ).execute()
    categories = results.get('files', [])

    # Dicionário para armazenar os IDs dos arquivos
    file_ids = {}

    # Itera sobre cada categoria
    for category in categories:
        # Verifica se o item é uma pasta (mimeType é 'application/vnd.google-apps.folder')
        if category['mimeType'] == 'application/vnd.google-apps.folder':
            # Obtém a lista de subpastas dentro da categoria
            subfolder_results = drive_service.files().list(
                q=f"'{category['id']}' in parents",
                fields="nextPageToken, files(id, name, mimeType)"
            ).execute()
            subfolders = subfolder_results.get('files', [])

            # Itera sobre cada subpasta
            for subfolder in subfolders:
                # Verifica se o item é uma pasta (mimeType é 'application/vnd.google-apps.folder')
                if subfolder['mimeType'] == 'application/vnd.google-apps.folder':
                    # Obtém a lista de arquivos na subpasta
                    results = drive_service.files().list(
                        q=f"'{subfolder['id']}' in parents",
                        fields="nextPageToken, files(id, name, mimeType)"
                    ).execute()
                    files = results.get('files', [])

                    # Adiciona os IDs dos arquivos ao dicionário e imprime os nomes dos arquivos
                    file_ids[subfolder['name']] = {}
                    for file in files:
                        if file['mimeType'] == 'application/json':  # Verifica se o arquivo é um arquivo JSON
                            file_ids[subfolder['name']][file['name']] = file['id']

    return file_ids

def carregar_dados(categoria, dados_file_id=None, trends_file_id=None):
    dados = None
    tendencias = None

    if dados_file_id is not None:
        # Carrega os dados
        dados = pd.read_json(f'https://drive.google.com/uc?export=download&id={dados_file_id}')

        # Remove as linhas com valores NaN
        dados = dados.dropna()

        # Imputa 'N/A' com -1
        dados['Visitas'].replace('N/A', -1, inplace=True)
        dados['Estrelas'].replace('N/A', -1, inplace=True)

    if trends_file_id is not None:
        # Lendo os dados das tendências salvos no bucket da cloud
        response = requests.get(f'https://drive.google.com/uc?export=download&id={trends_file_id}')
        trends_data = response.json()

        # Extrai apenas os valores da 'keyword' e armazena em uma lista
        tendencias = [item['keyword'] for sublist in trends_data for item in sublist]

    return dados, tendencias

# Função para plotar gráficos
def plotar_graficos(df):
    # Agrupa os dados por Grupo e calcula a mediana do Preço
    df_median = df.groupby('Grupo')['Preço'].median().reset_index()

    # Cria um gráfico de barras interativo com a mediana do preço por Grupo
    fig = go.Figure()

    for i, grupo in enumerate(df_median['Grupo']):
        fig.add_trace(go.Bar(
            x=[grupo],
            y=[df_median.loc[i, 'Preço']],
            text=df_median.loc[i, 'Preço'],
            textposition='auto',
            name=grupo
        ))

    # Atualiza o layout do gráfico para incluir a legenda interativa
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'},
                      hovermode="x", title="Mediana de Preço por Grupo")

    st.plotly_chart(fig)

# Sidebar
opcao = st.sidebar.selectbox('Escolha uma opção', ['Grupos', 'Trends'])

if opcao == 'Grupos':
    modelo = carregar_modelo()

    # Obtém os IDs dos arquivos
    file_ids = obter_ids_arquivos()

    categorias = list(file_ids.keys())
    categoria = st.selectbox('Escolha uma categoria', categorias)

    # Obtém o ID do arquivo 'dados.json' na categoria selecionada
    dados_file_id = file_ids[categoria]['dados.json']

    # Apenas os produtos
    dados, _ = carregar_dados(categoria, dados_file_id)

    # Novos dados
    X = dados[['Preço', 'Visitas', 'Estrelas']]

    # Obtém os rótulos dos clusters para os novos dados
    labels = modelo.predict(X)

    # Adiciona os rótulos dos clusters ao DataFrame de dados
    dados['Cluster'] = labels

    # Define um dicionário que mapeia os rótulos dos clusters para os nomes dos grupos
    cluster_names = {
    0: "Desconhecidos baratos",
    1: "Aclamados",
    2: "Baratos de qualidade variada"
}

    # Adiciona uma nova coluna 'Grupo' ao DataFrame que mapeia os rótulos dos clusters para os nomes dos grupos
    dados['Grupo'] = dados['Cluster'].map(cluster_names)

    # Gráficos
    plotar_graficos(dados)

    # Cria um widget de seleção para escolher um grupo
    grupos = dados['Grupo'].dropna().unique()
    grupo_selecionado = st.selectbox('Escolha um grupo', grupos)

    # Filtra o DataFrame para incluir apenas os itens do grupo selecionado
    dados_filtrados = dados[dados['Grupo'] == grupo_selecionado]

    # Transforma a coluna 'Link' em uma coluna de links clicáveis
    dados_filtrados['Link'] = dados_filtrados['Link'].apply(lambda x: f'<a href="{x}">Link</a>')

    # Remove as colunas especificadas
    dados_filtrados = dados_filtrados.drop(columns=['ID do produto','Categoria','Cluster','Grupo']).reset_index(drop=True)

    # Cria um widget de seleção para escolher uma marca
    marcas = dados_filtrados['Marca'].unique().tolist()
    marcas.insert(0, 'Todas')
    marca_selecionada = st.selectbox('Escolha uma marca', marcas)

    if marca_selecionada != 'Todas':
        dados_filtrados = dados_filtrados[dados_filtrados['Marca'] == marca_selecionada]

    # Cria um widget de controle deslizante para escolher um intervalo de preços
    preco_min = int(dados_filtrados['Preço'].min())
    preco_max = int(dados_filtrados['Preço'].max())

    if preco_min < preco_max:
        preco_range = st.slider('Escolha um intervalo de preços', min_value=preco_min, max_value=preco_max, value=(preco_min, preco_max))
        dados_filtrados = dados_filtrados[(dados_filtrados['Preço'] >= preco_range[0]) & (dados_filtrados['Preço'] <= preco_range[1])]

    # Mostra o DataFrame filtrado
    st.write(dados_filtrados.to_html(index=False,escape=False), unsafe_allow_html=True)

else:
    # Obtém os IDs dos arquivos
    file_ids = obter_ids_arquivos()

    categorias = list(file_ids.keys())
    categoria = st.selectbox('Escolha uma categoria', categorias)

    # Obtém o ID do arquivo 'tendencias.json' na categoria selecionada
    trends_file_id = file_ids[categoria]['tendencias.json']

    # Apenas trends
    _, trends = carregar_dados(categoria, trends_file_id=trends_file_id)

    # Exibe as tendências de forma apresentável
    for trend in trends:
        st.markdown(f"* {trend}")