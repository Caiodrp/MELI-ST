import boto3
import sagemaker
from sagemaker import get_execution_role
from sagemaker import KMeans
import pandas as pd
from sklearn.cluster import KMeans as SKLearnKMeans
from joblib import dump
import os

# Nome do bucket do S3 onde o modelo treinado será carregado
bucket_name = 'meu-bucket'

# Nome do modelo bucket
model_name = 'Modelo/model.joblib'

# Nome do modelo treinado
display_name = "kmeans-meli"

# Caminho para os dados de treinamento no S3
data_path = 's3://meu-bucket/Celulares e Telefones/dados.json'

# Número de clusters para o KMeans
n_clusters = 4

# Função para carregar os dados do S3
def load_data(data_path):
    print("Carregando os dados...")
    df = pd.read_json(data_path, lines=True)  # Lê os dados no formato JSON
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
    model = SKLearnKMeans(n_clusters=3, n_init=10, random_state=123)  # Inicializa o objeto KMeans
    model.fit(data)  # Treina o modelo KMeans com os dados
    print("Modelo treinado.")
    return model

# Função para fazer upload do modelo treinado para o S3
def upload_model(model, bucket_name, blob_name):
    print("Fazendo upload do modelo...")
    dump(model, 'model.joblib')  # Salva o modelo treinado em um arquivo joblib
    s3 = boto3.resource('s3')  # Inicializa o recurso do S3
    s3.meta.client.upload_file('model.joblib', bucket_name, blob_name)  # Faz upload do arquivo joblib para o S3
    print("Upload do modelo concluído.")

# Função principal que carrega os dados, pré-processa os dados, treina o modelo e faz upload do modelo
def main():
    data = load_data(data_path)  # Carrega os dados
    preprocessed_data = preprocess_data(data)  # Pré-processa os dados
    model = train_model(preprocessed_data, n_clusters)  # Treina o modelo
    upload_model(model, bucket_name, model_name)  # Faz upload do modelo

    print("Registrando o modelo...")
    # Inicializa o cliente do SageMaker
    sagemaker_session = sagemaker.Session()
    role = get_execution_role()

    # Define o local dos dados de treinamento
    data_location = 's3://{}/{}'.format(bucket_name, 'train')

    # Inicializa o objeto KMeans
    kmeans = KMeans(role=role,
                    instance_count=1,
                    instance_type='ml.c4.xlarge',
                    output_path='s3://{}/{}/output'.format(bucket_name, 'train'),
                    k=n_clusters,
                    sagemaker_session=sagemaker_session)

    # Treina o modelo KMeans
    kmeans.fit(kmeans.record_set(preprocessed_data))

    print("Criando o endpoint...")
    # Cria um endpoint para servir o modelo
    kmeans_predictor = kmeans.deploy(initial_instance_count=1,
                                     instance_type='ml.m4.xlarge')
    print("Endpoint criado.")

# Código para tornar o script executável
if __name__ == '__main__':
    main()
