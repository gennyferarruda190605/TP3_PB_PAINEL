import streamlit as st
from comum import carregar_df
import plotly.express as px
 
df = carregar_df()

# Inseri uma condição para que o usuário possa escolher as faixas etárias, regiões e ordenação do ranking, e assim visualizar a tabela filtrada e os gráficos de barras e linhas.
with st.sidebar:
    st.header('Seleção de Filtros 🔎')

    # Criando as variáveis no session state, para manter as opções dos filtros quando houver re-execuções da página 
    if 'faixas_selecionadas' not in st.session_state:
        st.session_state.faixas_selecionadas = ['faixa_10_a_14', 'faixa_15_a_19']

    if 'regioes_selecionadas' not in st.session_state:
        st.session_state.regioes_selecionadas = sorted(df['regiao'].unique())

    if 'ordenacao' not in st.session_state:
        st.session_state.ordenacao = 'Maior para menor'


    with st.form('filtros'):

        faixas = ['faixa_10_a_14', 'faixa_15_a_19']

        faixas_sel = st.multiselect(
            'Faixa etária',
            options=faixas,
            key='faixas_selecionadas',  
            help='Deixe vazio para incluir todas as faixas etárias.'
        )

        regioes_sel = st.multiselect(
            'Região',
            options=sorted(df['regiao'].unique()),
            key='regioes_selecionadas',  
            help='Deixe vazio para incluir todas as regiões.',
        )

        ordenacao = st.radio(
            'Ordenar ranking por',
            options=['Maior para menor', 'Menor para maior', 'Ordem alfabética (UF)'],
            key='ordenacao',  
            help='Escolha a forma de ordenação do ranking.',
        )
        
        aplicar = st.form_submit_button('Aplicar filtros')

    if st.button('Remover filtros'):

        st.session_state.faixas_selecionadas = ['faixa_10_a_14', 'faixa_15_a_19']
        st.session_state.regioes_selecionadas = sorted(df['regiao'].unique())
        st.session_state.ordenacao = 'Maior para menor'
        st.rerun()

    if aplicar:
        st.success('Filtros aplicados.')


# Criando um dataframe filtrado com base nas seleções do usuário, e ordenando de acordo com a escolha do usuário.

colunas_faixa_sel = faixas_sel if faixas_sel else faixas 
regioes_final = regioes_sel if regioes_sel else sorted(df['regiao'].unique())

df_filtrado = df[df['regiao'].isin(regioes_final)][['uf', 'regiao'] + colunas_faixa_sel]
df_filtrado['total_nascidos'] = df_filtrado[colunas_faixa_sel].sum(axis=1)

if ordenacao == 'Maior para menor':
    df_filtrado = df_filtrado.sort_values(by='total_nascidos', ascending=False)

elif ordenacao == 'Menor para maior':
    df_filtrado = df_filtrado.sort_values(by='total_nascidos', ascending=True)     

elif ordenacao == 'Ordem alfabética (UF)':
    df_filtrado = df_filtrado.sort_values(by='uf', ascending=True)  




st.header('Gráficos de Barras e Linhas 📊📈')

if colunas_faixa_sel:

    st.markdown(' ***Gráfico dos dados filtrados***')

    # Implementei dois checkboxes para que o usuário possa escolher se deseja visualizar o gráfico de barras, o gráfico de linhas ou ambos.
    check_barras = st.toggle('Exibir gráfico de barras', value=True)
    check_linhas = st.toggle('Exibir gráfico de linhas')


    if check_barras:
        st.subheader('Distribuição de Nascidos Vivos por Região e Faixa etária')
        st.bar_chart(
            df_filtrado,
            x='regiao',
            y=colunas_faixa_sel,
            y_label='Nascidos vivos',
            height=600,
            stack=False)

    if check_linhas:
        st.subheader('Distribuição de Nascidos Vivos por Região e Faixa etária')

        if len(regioes_sel) >= 2:

            st.line_chart(
                df_filtrado,
                x='regiao',
                y=colunas_faixa_sel,
                y_label='Nascidos vivos',
                height=600)

        
        else:
            st.info('Selecione pelo menos duas regiões para visualizar o gráfico de linhas.')

    else: 
        st.info('Selecione pelo menos uma opção de gráfico.')

st.divider()

st.subheader('Distribuição de Nascidos Vivos por Região')
st.caption('Todas as faixas étarias')

pizza = px.pie(
        df_filtrado, 
        names='regiao', 
        values='total_nascidos')

st.plotly_chart(pizza, use_container_width=True)
