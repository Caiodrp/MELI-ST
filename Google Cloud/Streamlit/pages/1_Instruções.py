import streamlit as st

# Definir o template
st.set_page_config(page_title='Instruções',
                page_icon='🛍️',
                layout='wide')

# Função principal para o corpo do script
def main():
    # Título centralizado
    st.write(
        '<div style="display:flex; align-items:center; justify-content:center;">'
        '<h1 style="font-size:4.5rem;">Instruções</h1>'
        '</div>',
        unsafe_allow_html=True
    )

    # Divisão
    st.write("---")

    # Adicionando texto antes do vídeo
    st.write("Este é um tutorial em vídeo sobre como usar a aplicação")

    # Adicionando vídeo
    st.write()
    st.write(
        '<div style="display:flex; align-items:center; justify-content:center;">'
        '<video width="560" height="315" controls>'
        '<source src="https://github.com/Caiodrp/Prever-ProducaoGas-ST/raw/main/tutorial.webm" type="video/webm">'
        '</video>'
        '</div>',
        unsafe_allow_html=True
    )

    # Informações sobre os dados
    st.write('Os dados foram obtidos a partir da API do Mercado Livre e armazenados na nuvem.')
    st.write('Eles foram transformados e agrupados utilizando o algoritmo de Machine Learning KMeans.')

    # Adicionando texto
    st.write(
        """
        # Clusterização e Análise

        Na página "Clusterização e Análise", você pode visualizar diferentes informações sobre os produtos disponíveis no Mercado Livre. 

        ### Grupos

        Esta parte faz a clusterização dos produtos utilizando o algoritmo de Machine Learning KMeans. Os produtos são agrupados em diferentes categorias com base em suas características. Você pode escolher visualizar os produtos por preço, popularidade e qualidade. Além disso, você pode ser redirecionado para a página do produto clicando no link associado.

        ### Trends

        A subseção "Trends" mostra as palavras-chave mais buscadas pelos usuários do Mercado Livre por categoria.
        
        """
    )

# Chamar a função principal
if __name__ == '__main__':
    main()