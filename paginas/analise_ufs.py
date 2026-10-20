import streamlit as st
from comum import carregar_df
import plotly.express as px

df = carregar_df()

st.header('Análise por UFs')


st.header('Soma total de casos no Brasil em 2023 por grupo de faixa étaria ')

col1, col2, col3 = st.columns(3)
with col1:
    st.metric('Soma total - 10 a 14 anos', df['faixa_10_a_14'].sum())
with col2:
    st.metric('Soma total - 15 a 19 anos', df['faixa_15_a_19'].sum())
with col3:
    st.metric(' Quantidade de UF na amostra', len(df))

st.divider()
 


st.header('Distribuição de Nascidos Vivos')

todos_ufs = st.selectbox(
            'Escolha se deseja visualizar todos ou Escolher as UF', 
            options=['Todos', 'Selecionar UFs'])


if todos_ufs == 'Todos':

    pizza_uf = px.pie(
            df, 
            names='uf', 
            values='total_nascidos')
    
    st.plotly_chart(pizza_uf, use_container_width=True)


if todos_ufs == 'Selecionar UFs':

    if 'ufs_selecionadas' not in st.session_state:
        st.session_state.ufs_selecionadas = sorted(df['uf'].unique())

    ufs_selec = st.multiselect(
                'Selecione as UFs', 
                options=sorted(df['uf'].unique()), 
                default=sorted(df['uf'].unique()),
                key='ufs_selecionadas')

    if ufs_selec:
        pizza_uf = px.pie(
                    df[df['uf'].isin(ufs_selec)], 
                    names='uf', values='total_nascidos')
        
        st.plotly_chart(pizza_uf, use_container_width=True)

    else:
        st.info('Selecione pelo menos uma UF para visualizar o gráfico de pizza.')


st.header('Tabela de Dados 📋')
st.dataframe(df, use_container_width=True)

