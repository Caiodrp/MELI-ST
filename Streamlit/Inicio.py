import streamlit as st

# Definir o template
st.set_page_config(page_title='Início',
                page_icon='🛍️',
                layout='wide')

def main():
    # Apresenta a imagem na barra lateral da aplicação
    url = "https://github.com/Caiodrp/MELI-ST/blob/main/img/Design%20sem%20nome.jpg?raw=true"
    st.sidebar.image(url,use_column_width=True)

    # Título centralizado
    st.write(
        '<div style="display:flex; align-items:center; justify-content:center;">'
        '<h1 style="font-size:4.5rem;">Pesquisa de Mercado com o Mercado Livre</h1>'
        '</div>',
        unsafe_allow_html=True
    )

    # Subtítulo
    st.write(
        '<div style="display:flex; align-items:center; justify-content:center;">'
        '<h2 style="font-size:2.5rem;">Descubra as melhores oportunidades no Mercado Livre com Machine Learning</h2>'
        '</div>',
        unsafe_allow_html=True
    )

    # Divisão
    st.write("---")

    # Imagem do lado da explicação
    col1, col2 = st.columns(2)

    col1.write(
        "<p style='font-size:1.5rem;'> Esta aplicação web é uma <b>ferramenta de pesquisa de mercado</b> que utiliza um algoritmo de Machine Learning para separar os itens disponíveis no site do Mercado Livre em grupos, a fim de descobrir as melhores oportunidades."
        "<br>"
        "A aplicação traz as melhores oportunidades do dia por categoria, além das palavras-chave mais buscadas por consumidores, e também informações estatísticas de marcas e preços.</p>",
        unsafe_allow_html=True
    )

    col2.write(
        '<div style="position:relative;"><iframe src="https://giphy.com/embed/AHE816ZwolOAOGzsvT" width="480" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe></div>',
        unsafe_allow_html=True
    )

    # Divisão
    st.write("---")

    st.write(
        '<h3 style="text-align:left;">Autor</h3>'
        '<ul style="list-style-type: disc; margin-left: 20px;">'
        '<li>Seu Nome</li>'
        '<li><a href="https://github.com/seu_usuario_github">GitHub</a></li>'
        '</ul>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
