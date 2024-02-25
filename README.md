
# Pesquisa de Mercado no Mercado Livre com Pipeline na Nuvem e ML

Esse projeto utiliza o Apache Airflow para extrair dados da API do Mercado Livre, armazena esses dados em um Data Lake na nuvem, processa os dados com um modelo de Machine Learning (K-means) e apresenta os resultados no Streamlit

![Fluxo API-MELI](https://github.com/Caiodrp/MELI-ST/assets/99834159/efb14145-d5dd-4374-a3a3-79d2a6f23781)

Abaixo, você encontrará um vídeo demonstrando o funcionamento da aplicação.

https://github.com/Caiodrp/MELI-ST/assets/99834159/c3e6e267-861d-4d20-af79-1e0f07c245b6

## Possíveis Usos

Este projeto pode ser extremamente útil para vários públicos. Por exemplo:

- **Vendedores**: Podem usar as informações para entender quais produtos estão em alta demanda, ajudando-os a ajustar seu inventário e estratégias de preços.
- **Compradores**: Podem usar o sistema para encontrar produtos semelhantes ou para entender as tendências do mercado, ajudando-os a fazer compras mais informadas.
- **Analistas de Mercado**: Podem usar os dados para realizar análises mais profundas do mercado do Mercado Livre.

## Plataformas

### AWS

1. **Extração de Dados**: Utilize o Airflow no Amazon Managed Workflows for Apache Airflow (MWAA) para orquestrar a extração de dados da API do Mercado Livre.
2. **Armazenamento de Dados**: Armazene os dados extraídos no Amazon S3, que atuará como seu Data Lake.
3. **Processamento de Dados**: Use o Amazon SageMaker para criar e treinar seu modelo de Machine Learning (K-means). Depois de treinado, crie um endpoint no SageMaker para disponibilizar seu modelo.
4. **Apresentação dos Resultados**: Use o Streamlit para criar uma aplicação web que apresenta os resultados da análise de dados.

### GCP

1. **Extração de Dados**: Utilize o Airflow no Google Cloud Composer para orquestrar a extração de dados da API do Mercado Livre.
2. **Armazenamento de Dados**: Armazene os dados extraídos no Google Cloud Storage (GCS), que atuará como seu Data Lake.
3. **Processamento de Dados**: Use o Google Vertex AI para criar e treinar seu modelo de Machine Learning (K-means). Depois de treinado, crie um endpoint no Vertex AI para disponibilizar seu modelo.
4. **Apresentação dos Resultados**: Use o Streamlit para criar uma aplicação web que apresenta os resultados da análise de dados.

### Modo Gratuito

1. **Extração de Dados**: Configure uma instância local do Airflow para orquestrar a extração de dados da API do Mercado Livre.
2. **Armazenamento de Dados**: Armazene os dados extraídos no Google Drive, que atuará como seu Data Lake.
3. **Processamento de Dados**: Carregue seu modelo de Machine Learning (K-means) como um objeto em sua aplicação.
4. **Apresentação dos Resultados**: Use o Streamlit para criar uma aplicação web que apresenta os resultados da análise de dados.

