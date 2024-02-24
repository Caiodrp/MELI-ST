
# Pesquisa de Mercado no Mercado Livre com Pipeline na Nuvem e ML

O projeto começa com a extração de dados da API do Mercado Livre. Essa extração é orquestrada pelo Apache Airflow, uma ferramenta poderosa para criar, monitorar e ajustar pipelines de dados. O Airflow permite que você programe a extração de dados para ocorrer em intervalos regulares, garantindo que você sempre tenha os dados mais recentes disponíveis para análise.

Os dados extraídos são então armazenados em um Data Lake na nuvem. Um Data Lake é um repositório de armazenamento que mantém dados em seu formato bruto, permitindo que você armazene grandes volumes de dados não estruturados ou semi-estruturados. Isso é especialmente útil quando se lida com uma grande variedade de produtos e compradores, como no caso do Mercado Livre.

Uma vez armazenados, os dados são processados por um modelo de Machine Learning. Especificamente, um algoritmo de K-means é usado para agrupar os produtos em clusters. Isso facilita a busca de produtos semelhantes e ajuda a entender as tendências do mercado.

Finalmente, os resultados são apresentados no Streamlit, uma ferramenta que permite criar rapidamente aplicativos web personalizados para Machine Learning e ciência de dados. Isso pode incluir a visualização dos clusters de produtos, bem como as tendências diárias de demanda por categoria.

Esse fluxo permite que o projeto forneça insights valiosos sobre as tendências do mercado no Mercado Livre, que podem ser úteis para vendedores que desejam ajustar seu inventário e estratégias de preços, compradores que desejam fazer compras mais informadas e analistas de mercado que desejam realizar análises mais profundas.


![Fluxo API-MELI](https://github.com/Caiodrp/MELI-ST/assets/99834159/10c140de-688e-4088-9d19-c606d3894d0e)


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

