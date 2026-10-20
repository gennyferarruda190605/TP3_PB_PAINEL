import pandas as pd
import streamlit as st
import os
import requests

from src.data_access2 import obter_frases

regioes_map = {
    1: 'Norte',
    2: 'Nordeste',
    3: 'Sudeste',
    4: 'Sul',
    5: 'Centro-Oeste'}


chaves_preservadas = (
    'faixas_selecionadas',    
    'regioes_selecionadas',
    'ordenacao',
    'modo_pizza_uf',          
    'ufs_selecionadas',
    'faixas_regioes',         
    'check_barras',
    'check_linhas',
    'sep_csv',                
    'col_frases',
    'eixo_x_up',
    'eixo_y_up')




url_apli = os.getenv('url_apli', 'http://127.0.0.1:8000')

# Requerimento da API que criei, para utilizar no painel
@st.cache_data(ttl=3600)
def organizar_df():
    resposta = requests.get(
        f'{url_apli}/natalidade',
        params={'limite': 27},
        timeout=10)
    resposta.raise_for_status()

    dados = resposta.json()['dados']
    df = pd.DataFrame(dados)
    df['regiao'] = (df['id'] // 10).map(regioes_map)
    df['total_nascidos'] = df['faixa_10_a_14'] + df['faixa_15_a_19']
    return df


@st.cache_data(ttl=3600)
def carregar_df():

    try:
        return organizar_df()
    except FileNotFoundError:
        st.error('Erro: arquivo não foi encontrado. Verifique o arquivo.')
        st.stop()



@st.cache_data(ttl=3600)
def carregar_frases():
    try:
        return obter_frases()
    except FileNotFoundError:
        st.error('Erro: arquivo não foi encontrado. Verifique o arquivo.')
        st.stop()



def inicializar_estado() -> None:

    st.session_state.setdefault('df_enviado', None)     
    st.session_state.setdefault('nome_arquivo', None)
    st.session_state.setdefault('df_mesclado', None)



def preservar_filtros() -> None:

    for chave in chaves_preservadas:
        if chave in st.session_state:
            st.session_state[chave] = st.session_state[chave]