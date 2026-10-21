
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from comum import carregar_frases
from src.analise_texto import estatisticas, frequencia, gerar_nuvem, stop_words

frases = carregar_frases()
texto = ' '.join(frases)

st.header('Notícia 2023 - Portal SCP📰')
st.subheader('*Gravidez na adolescência: um desafio de saúde pública que exige o olhar atento da pediatria*')
st.caption('*Fonte: [SCP - Sociedade Catarinense de Pediatria](https://www.scp.org.br/gravidez-na-adolescencia-um-desafio-de-saude-publi++ca-que-exige-o-olhar-atento-da-pediatria/)*')

st.divider()
st.subheader('Estatísticas 📉')

stats = estatisticas(texto)

c1, c2, c3, c4 = st.columns(4)
c1.metric('Caracteres', stats['caracteres'])
c2.metric('Palavras', stats['palavras'])
c3.metric('Palavras úteis', stats['palavras_uteis'])
c4.metric('Vocabulário', stats['vocabulario'])

st.divider()
st.subheader('Palavras mais frequentes🏆')

df_freq = pd.DataFrame(frequencia(texto, 15))
st.bar_chart(df_freq.set_index('palavra'))

st.divider()
st.subheader('Nuvem de palavras ☁️')

nuvem = gerar_nuvem(texto, stop_words)
fig, ax = plt.subplots()

ax.imshow(nuvem, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)

st.divider()

st.subheader('Tabela de palavras')
st.dataframe(df_freq, hide_index=True)

st.subheader('Download da tabela de palavras⬇️')
st.download_button(label='Tabela em CSV', data=df_freq.to_csv(index=False).encode('utf-8-sig'), file_name='noticias_gravidez_adolescente.csv')