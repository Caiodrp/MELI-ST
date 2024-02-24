from google.cloud import aiplatform
from google.cloud.aiplatform import gapic as aip
import pandas as pd
from sklearn.cluster import KMeans
from joblib import dump
from google.cloud import storage
from gcsfs import GCSFileSystem
from sklearn.preprocessing import StandardScaler

# ID do seu projeto
project_id = 'deft-approach-412320'

# Localização do seu projeto
location = 'southamerica-east1'

# Caminho para os dados de treinamento no Google Cloud Storage
data_path = 'gs://itens-meli/Celulares e Telefones/dados.json'

# Número de clusters para o KMeans
n_clusters = 3

# Nome do bucket do Google Cloud Storage onde o modelo treinado será carregado
bucket_name = 'itens-meli'

# Nome do modelo bucket
model_name = 'Modelo/model.joblib'

# Nome do modelo treinado
display_name = "kmeans-meli"

# Caminho para o modelo treinado no Google Cloud Storage
artifact_uri = "gs://itens-meli/Modelo"

# Imagem do contêiner para treinamento e previsão
serving_container_image_uri = "us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-3:latest"

# Função para carregar os dados do Google Cloud Storage
def load_data(data_path):
    print("Carregando os dados...")
    fs = GCSFileSystem(project=project_id)  # Inicializa o sistema de arquivos do Google Cloud Storage
    with fs.open(data_path) as dados:  # Abre o arquivo de dados
        df = pd.read_json(dados)  # Lê os dados no formato JSON
    print("Dados carregados.")
    return df

# Função para pré-processar os dados
def preprocess_data(df):
    print("Pré-processando os dados...")
    df = df.dropna()  # Remove as linhas com valores NaN
    df.loc[df['Visitas'] == 'N/A', 'Visitas'] = -1  # Substitui 'N/A' por -1 na coluna 'Visitas'
    df.loc[df['Estrelas'] == 'N/A', 'Estrelas'] = -1  # Substitui 'N/A' por -1 na coluna 'Estrelas'
    X = df[['Preço', 'Visitas', 'Estrelas']]  # Seleciona as colunas para treinamento
    print("Dados pré-processados.")
    return X

# Função para treinar o modelo KMeans
def train_model(data, n_clusters):
    print("Treinando o modelo...")
    model = KMeans(n_clusters=n_clusters, n_init=10, random_state=123)  # Inicializa o objeto KMeans
    model.fit(data)  # Treina o modelo KMeans com os dados
    print("Modelo treinado.")
    return model

# Função para fazer upload do modelo treinado para o Google Cloud Storage
def upload_model(model, bucket_name, blob_name):
    print("Fazendo upload do modelo...")
    dump(model, 'model.joblib')  # Salva o modelo treinado em um arquivo joblib
    storage_client = storage.Client()  # Inicializa o cliente do Google Cloud Storage
    bucket = storage_client.bucket(bucket_name)  # Obtém o bucket do Google Cloud Storage
    blob = bucket.blob(blob_name)  # Cria um novo blob no bucket
    blob.upload_from_filename('model.joblib')  # Faz upload do arquivo joblib para o blob
    print("Upload do modelo concluído.")

# Função principal que carrega os dados, pré-processa os dados, treina o modelo e faz upload do modelo
def main():
    data = load_data(data_path)  # Carrega os dados
    preprocessed_data = preprocess_data(data)  # Pré-processa os dados
    model = train_model(preprocessed_data, n_clusters)  # Treina o modelo
    upload_model(model, bucket_name, model_name)  # Faz upload do modelo

    print("Registrando o modelo...")
    # Inicializa o cliente do Vertex AI
    aiplatform.init(project=project_id, location=location)

    # Registra o modelo treinado
    model = aiplatform.Model.upload(
        display_name=display_name,
        artifact_uri=artifact_uri,
        serving_container_image_uri=serving_container_image_uri,
    )
    print("Modelo registrado.")

    print("Criando o endpoint...")
    # Cria um endpoint para servir o modelo
    endpoint = aiplatform.Endpoint.create(display_name="kmeansmeli-endpoint")
    print("Endpoint criado.")

    print("Implantando o modelo...")
    # Implanta o modelo no endpoint
    endpoint.deploy(model=model)
    print("Modelo implantado.")

# Código para tornar o script executável
if __name__ == '__main__':
    main()
