import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import boto3
import numpy as np

# Nome do bucket do S3 onde os dados estão armazenados
bucket_name = 'meu-bucket'

# Nome do endpoint do modelo
endpoint_name = 'nome-do-endpoint'

# Função para configurar o endpoint do modelo
@st.cache_resource
def configurar_endpoint_modelo():
    sagemaker_runtime = boto3.client('sagemaker-runtime')
    return sagemaker_runtime

# Função para carregar os dados do S3
def load_data(category, file_name):
    print("Carregando os dados...")
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket_name, Key=f'{category}/{file_name}')
    df = pd.read_json(obj['Body'], lines=True)  # Lê os dados no formato JSON
    print("Dados carregados.")
    return df

# Função para fazer previsões usando o modelo no endpoint
def predict(modelo, data):
    print("Fazendo previsões...")
    response = modelo.invoke_endpoint(EndpointName=endpoint_name, ContentType='text/csv', Body=data.to_csv(header=False, index=False))
    labels = np.fromstring(response['Body'].read(), sep=',')
    print("Previsões concluídas.")
    return labels

# Função para plotar gráficos
def plotar_graficos(df):
    # Agrupa os dados por Grupo e calcula a média do Preço
    df_median = df.groupby('Grupo')['Preço'].median().reset_index()

    # Cria um gráfico de barras interativo com a média do preço por Grupo
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

# Função principal para o corpo do script
def main():
    # Sidebar
    opcao = st.sidebar.selectbox('Escolha uma opção', ['Grupos', 'Trends'])

    if opcao == 'Grupos':
        modelo = configurar_endpoint_modelo()

        # Obtém as categorias
        s3 = boto3.resource('s3')
        my_bucket = s3.Bucket(bucket_name)
        categorias = [obj.key.split('/')[0] for obj in my_bucket.objects.all()]

        categoria = st.selectbox('Escolha uma categoria', categorias)

        # Apenas os produtos
        dados = load_data(categoria, 'dados.json')

        # Novos dados
        X = dados[['Preço', 'Visitas', 'Estrelas']]

        # Obtém os rótulos dos clusters para os novos dados
        labels = predict(modelo, X)

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
        modelo = configurar_endpoint_modelo()

        # Obtém as categorias
        s3 = boto3.resource('s3')
        my_bucket = s3.Bucket(bucket_name)
        categorias = [obj.key.split('/')[0] for obj in my_bucket.objects.all()]

        categoria = st.selectbox('Escolha uma categoria', categorias)

        # Apenas trends
        trends = load_data(categoria, 'tendencias.json')

        # Exibe as tendências de forma apresentável
        for trend in trends:
            st.markdown(f"* {trend}")