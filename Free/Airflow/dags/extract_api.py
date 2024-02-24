import requests
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from concurrent.futures import ThreadPoolExecutor
from google.cloud import storage

# Define o token de acesso para a API do Mercado Livre
access_token = "TEST-2969247859351650-040913-40a7d3b106f15311382c698055a26008-244124958"

# Lista de categorias
categories = [
    {"id": "MLB5672", "name": "Acessórios para Veículos"},
    {"id": "MLB271599", "name": "Agro"},
    {"id": "MLB1403", "name": "Alimentos e Bebidas"},
    {"id": "MLB1071", "name": "Animais"},
    {"id": "MLB1367", "name": "Antiguidades e Coleções"},
    {"id": "MLB1368", "name": "Arte, Papelaria e Armarinho"},
    {"id": "MLB1384", "name": "Bebês"},
    {"id": "MLB1246", "name": "Beleza e Cuidado Pessoal"},
    {"id": "MLB1132", "name": "Brinquedos e Hobbies"},
    {"id": "MLB1430", "name": "Calçados, Roupas e Bolsas"},
    {"id": "MLB1039", "name": "Câmeras e Acessórios"},
    {"id": "MLB1743", "name": "Carros, Motos e Outros"},
    {"id": "MLB1574", "name": "Casa, Móveis e Decoração"},
    {"id": "MLB1051", "name": "Celulares e Telefones"},
    {"id": "MLB1500", "name": "Construção"},
    {"id": "MLB5726", "name": "Eletrodomésticos"},
    {"id": "MLB1000", "name": "Eletrônicos, Áudio e Vídeo"},
    {"id": "MLB1276", "name": "Esportes e Fitness"},
    {"id": "MLB263532", "name": "Ferramentas"},
    {"id": "MLB12404", "name": "Festas e Lembrancinhas"},
    {"id": "MLB1144", "name": "Games"},
    {"id": "MLB1459", "name": "Imóveis"},
    {"id": "MLB1499", "name": "Indústria e Comércio"},
    {"id": "MLB1648", "name": "Informática"},
    {"id": "MLB218519", "name": "Ingressos"},
    {"id": "MLB1182", "name": "Instrumentos Musicais"},
    {"id": "MLB3937", "name": "Joias e Relógios"},
    {"id": "MLB1196", "name": "Livros, Revistas e Comics"},
    {"id": "MLB1168", "name": "Música, Filmes e Seriados"},
    {"id": "MLB264586", "name": "Saúde"},
    {"id": "MLB1540", "name": "Serviços"},
    {"id": "MLB1953", "name": "Mais Categorias"}
]

# Autenticação com o Google Drive
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Cria um servidor web local e lida com a autenticação.
drive = GoogleDrive(gauth)

# Função para criar uma pasta no Google Drive se ela ainda não existir
def create_folder_if_not_exists(folder_name):
    folders = drive.ListFile({'q': f"title='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    if len(folders) == 0:
        folder = drive.CreateFile({'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder'})
        folder.Upload()
        return folder
    else:
        return folders[0]

# Define a função para buscar os dados do produto
def fetch_product_data(product, index, category):
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"https://api.mercadolibre.com/items/{product['id']}/visits/time_window?last=7&unit=day"
        response = requests.get(url, headers=headers)
        visits_data = response.json()
        url = f"https://api.mercadolibre.com/reviews/item/{product['id']}"
        response = requests.get(url, headers=headers)
        reviews_data = response.json()
        brand = next((attr['value_name'] for attr in product['attributes'] if attr['id'] == 'BRAND'), 'N/A')
        model = next((attr['value_name'] for attr in product['attributes'] if attr['id'] == 'MODEL'), 'N/A')
        new_row = {
            "ID do produto": product['id'],
            "Preço": product['price'],
            "Marca": brand,
            "Modelo": model,
            "Link": product['permalink'],
            "Título": product['title'],
            "Categoria": category['name'],
            "Visitas": visits_data['total_visits'] if 'total_visits' in visits_data else 'N/A',
            "Estrelas": reviews_data['rating_average'] if 'rating_average' in reviews_data else 'N/A'
        }
        return new_row
    except Exception as e:
        print(f"Error processing product {index}: {e}")
        return None

def main():
    # Cria a pasta 'itens-meli' se ela ainda não existir
    parent_folder = create_folder_if_not_exists('itens-meli')

    # Inicializa o cliente de armazenamento
    storage_client = storage.Client()

    # Itera sobre as categorias
    for category in categories:
        # Inicializa a lista para armazenar os dados
        data = []
        trends = []  # Lista para armazenar as tendências

        # Inicializa o offset e o limite
        offset = 0
        limit = 50  # O limite é 50

        # Define os cabeçalhos para as solicitações
        headers = {"Authorization": f"Bearer {access_token}"}

        # Faz 20 chamadas à API para obter 1000 produtos
        for i in range(20):
            # Busca os produtos
            url = f"https://api.mercadolibre.com/sites/MLB/search?category={category['id']}&ITEM_CONDITION=2230284&offset={offset}&limit={limit}"
            response = requests.get(url, headers=headers)
            products = response.json()

            # Processa cada produto individualmente
            with ThreadPoolExecutor(max_workers=6) as executor:
                new_rows = list(executor.map(fetch_product_data, products.get('results', []), range(len(products.get('results', []))), [category]*len(products.get('results', []))))

            # Adiciona as novas linhas à lista de dados
            data.extend([row for row in new_rows if row is not None])

            # Atualiza o offset
            offset += limit

        # Busca as tendências para a categoria
        url = f"https://api.mercadolibre.com/trends/MLB/{category['id']}"
        response = requests.get(url, headers=headers)
        trends_data = response.json()

        # Adiciona as tendências à lista de tendências
        trends.append(trends_data)

        # Converte a lista de dados em uma string JSON
        json_data = json.dumps(data)
        json_trends = json.dumps(trends)  # Converte a lista de tendências em uma string JSON

        # Cria uma pasta para a categoria se ela ainda não existir
        category_folder = create_folder_if_not_exists(f'{parent_folder["id"]}/{category["name"]}')

        # Substitua 'meu-bucket' pelo nome do seu bucket e 'meus-dados.json' pelo nome desejado para o arquivo .json
        bucket = storage_client.bucket('itens-meli')
        blob = bucket.blob(f'{category["name"]}/dados.json')
        blob_trends = bucket.blob(f'{category["name"]}/tendencias.json')  # Blob para as tendências

        # Verifica se o blob já existe
        if not blob.exists():
            # Se o blob não existir, faz o upload dos dados
            blob.upload_from_string(json_data)
        else:
            # Se o blob existir, baixa os dados existentes
            existing_data = json.loads(blob.download_as_text())
            
            # Adiciona apenas os novos produtos
            existing_ids = {item['ID do produto'] for item in existing_data if isinstance(item, dict) and 'ID do produto' in item}
            new_data = [item for item in data if isinstance(item, dict) and 'ID do produto' in item and item['ID do produto'] not in existing_ids]
            
            # Atualiza os dados existentes com os novos produtos
            existing_data.extend(new_data)
            
            # Faz o upload dos dados atualizados
            blob.upload_from_string(json.dumps(existing_data))

        # Faz o upload das tendências
        blob_trends.upload_from_string(json_trends)

# Chama a função principal
if __name__ == "__main__":
    main()
