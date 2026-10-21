import streamlit as st
from comum import carregar_df
from comum import carregar_frases

 
frases = carregar_frases()

st.header('Tabela de Dados - Fonte Agregados do IBGE (SIDRA)')
df = carregar_df()
st.dataframe(df)

st.subheader('Download da Tabela de Dados ⬇️')
st.download_button(label='Tabela em CSV', data=df.to_csv(index=False).encode('utf-8-sig'), file_name='noticias_gravidez_adolescente.csv')
st.divider()

st.header('Noticías - Fonte Portal SCP ')

st.subheader('Download dos arquivo em CSV ⬇️')
st.download_button(label='Notícia completa em CSV', data='\n'.join(frases), file_name='noticias_gravidez_adolescente.csv')