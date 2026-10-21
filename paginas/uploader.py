import streamlit as st
from comum import carregar_frases
from src.analise_csv_uploader import ler_csv, mesclar_frases



frases = carregar_frases()


# Criando a variável no session state (Nunca em cachê, pois como disse em aula, arquivos enviados por terceiros não são confiáveis)
if 'df_enviado' not in st.session_state:
    st.session_state.df_enviado = None


st.header('Uploader de arquivo (CSV) ⬆️')

arquivo = st.file_uploader('Envie um arquivo CSV', type=['csv'])
sep = st.text_input('Separador do CSV', value=',', key='sep_csv')

if arquivo is not None:
    df_up, erro = ler_csv(arquivo.getvalue(), sep)

    if erro:
        st.error(erro)

    else:
        st.session_state.df_enviado = df_up
        st.success(f'Arquivo "{arquivo.name}" carregado: {len(df_up)} linhas, {df_up.shape[1]} colunas.')

df_up = st.session_state.df_enviado


if st.button('Remover arquivo 🗑️'):
    st.session_state.df_enviado = None
    st.rerun()

st.divider()

if 'df_mesclado' not in st.session_state:
    st.session_state.df_mesclado = None

if df_up is not None:

    #   Criei colunas para textos e números, já que não sei se serão dados em texto ou númericos. 
    colunas_texto = df_up.select_dtypes(include='object').columns.tolist()
    colunas_num = df_up.select_dtypes(include='number').columns.tolist()

    if colunas_texto:

        st.subheader('Deseja mesclar os dados? 🔀📋')
        col_frases = st.selectbox(
            'Coluna de texto para somar às frases', 
            colunas_texto, 
            key='col_frases')

        # Criando uma variável no session state para o df com os dados mesclados
        if 'df_mesclado' not in st.session_state:
            st.session_state.df_mesclado = None

        if st.button('Mesclar dados (Notícia + dados do arquivo)'):
            frases_enviadas = df_up[col_frases].dropna().astype(str).tolist()
            st.session_state.df_mesclado = mesclar_frases(frases, frases_enviadas)

        if st.session_state.df_mesclado is not None:
            st.divider()
            st.subheader('Dados Mesclados📋')
            st.dataframe(st.session_state.df_mesclado, hide_index=True)


    if colunas_num:
        st.divider()
        st.subheader('Gráfico de Barras com os dados enviados 📊')

        eixo_x = st.selectbox(
            'Coluna para o eixo X', 
            ['(índice)'] + colunas_texto, 
            key='eixo_x_up')
        
        eixo_y = st.selectbox(
            'Coluna numérica', 
            colunas_num, 
            key='eixo_y_up')
        
        dados = df_up if eixo_x == '(índice)' else df_up.set_index(eixo_x)
        st.bar_chart(dados[eixo_y])


    st.subheader(f' Tabela do Arquivo {arquivo.name} 📋')
    st.dataframe(df_up)