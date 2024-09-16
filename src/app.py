import streamlit as st
import pandas as pd
import time
import plotly.express as px

st.set_page_config(page_title='TP3 Dev Front-End ST', page_icon='📊', layout='wide', initial_sidebar_state='auto')

st.sidebar.header('Menu')
tab = st.sidebar.selectbox('Selecione uma opção', ['Introdução', 'Análise de Dados'])

if tab == 'Introdução':
    st.title('Introdução à aplicação')
    colormap = {   
        'Black': '#000000',
        'White': '#FFFFFF',
        'Gray': '#808080',     
        'Red': '#FF0000',
        'Blue': '#0000FF',
        'Green': '#00FF00',
        'Yellow': '#FFFF00',
        'Orange': '#FFA500',
        'Purple': '#800080',
        'Pink': '#FFC0CB',
        'Brown': '#A52A2A',
        'Navy': '#000080',
        'Cyan': '#00FFFF',
        'Magenta': '#FF00FF',
        'Gold': '#FFD700',
        'Silver': '#C0C0C0',
    }
    st.markdown(f'''
    <style>
    .stApp {{
        background-color: {colormap[st.selectbox('Escolha uma cor para o background:', list(colormap.keys()))]};
    }}
    </style>
    ''', unsafe_allow_html=True)

    font_color = ["Azul", "Verde", "Laranja", "Vermelho", "Violeta", "Cinza", "Arco-íris"]
    cores = ['blue', 'green', 'orange', 'red', 'violet', 'gray', 'rainbow']
    font = st.selectbox('Escolha uma cor para o texto:', font_color)
    for element in font_color:
        if font == element:
            escolha = cores[font_color.index(element)]

    st.write(f""":{escolha}[Neste projeto, você poderá fazer o upload de um arquivo de dados e visualizá-los em gráficos e tabelas.
              Escolhi o arquivo que contém a quantidade de estabelecimentos de hospedagem e unidades habitacionais no Brasil em 2016 porque ele fornece informações relevantes sobre a infraestrutura hoteleira do país naquele ano. Com esses dados, é possível analisar a distribuição geográfica dos estabelecimentos e unidades habitacionais, identificar tendências, e obter insights sobre o setor de hospedagem no Brasil. Além disso, a visualização dos dados por meio de gráficos e tabelas facilita a compreensão e interpretação das informações, permitindo uma análise mais detalhada e uma melhor tomada de decisões.
              Navegue pelo menu à esquerda para explorar os dados e visualizações disponíveis. Você poderá filtrar tabelas e baixar os dados para análises futuras.
              Foi utilizado neste código a I.A Copilot do GitHub para debugging.]""")

    
else:
    upload = st.file_uploader('Upload Arquivo Data Rio')

    @st.cache_data
    def read_excel_data(upload, header=0):
        return pd.read_excel(upload, header=header)

    if upload:
        raw_graf = read_excel_data(upload)
        st.write(raw_graf['Data.Rio'][1])
        details = st.button("Detalhes")
        if details:
            prog = st.progress(0)
            for counter in range(1, 101):
                time.sleep(0.1)                   
                prog.progress(counter)
            doc_details = {
                'Nome do Arquivo': upload.name,
                'Tamanho': upload.size,
                'Tipo': upload.type
            }
            st.write(doc_details)
        graf = read_excel_data(upload, header=4)
        if st.checkbox("Mostrar Dados Completos"):
            with st.spinner("Carregando..."):
                time.sleep(3)
            st.dataframe(graf)
            dl = st.download_button('Download', data=graf.to_csv(), file_name='data.csv', mime='text/csv')

        with st.expander("Visualizar Dados por Coluna"):
            select_box = st.selectbox("Selecione uma coluna para exibir:", graf.columns.tolist())
            if select_box:    
                st.write(graf[select_box])
                st.download_button('Download Coluna', data=graf.to_csv(), file_name='data.csv', mime='text/csv')

        with st.expander("Mostrar Certas Colunas"):
            multi = st.multiselect("Selecione as colunas", graf.columns.tolist())
            if multi:
                st.write(graf[multi])

        if graf.columns[1] == 'Município \n(Capital)':
            graf.columns = ['Municipio' if col == 'Município \n(Capital)' else col for col in graf.columns]

        fig = px.histogram(graf, x=graf.columns[1], y=graf.columns[7])
        st.plotly_chart(fig)
        fig2 = px.histogram(graf, x=graf.columns[1], y=graf.columns[3])
        st.plotly_chart(fig2)

        col=st.columns(2)

        col[0].metric("Total Estabelecimentos de Hospedagem", graf[graf.columns[3]][2])
        col[1].metric("Total de Unidades Habitacionais", graf[graf.columns[7]][2])

        if "upload" not in st.session_state:
            st.session_state["upload"] = raw_graf
        if "complete" not in st.session_state:
            st.session_state["complete"] = graf
        if "coluna" not in st.session_state:
            st.session_state["coluna"] = graf[select_box]
        if "multi" not in st.session_state:
            st.session_state["multi"] = graf[multi]

    else:
        st.write("Por favor, faça o upload do arquivo para visualizar os dados.")