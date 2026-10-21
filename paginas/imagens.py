import streamlit as st
from src.coleta_web2 import obter_imagens, obter_texto
import re
from comum import carregar_df



imagens = obter_imagens()
df = carregar_df()
textos = obter_texto()

st.header('Notícia 2024 - PORTAL UNFPA  ')
st.markdown(f'### *{textos[0]}*')
st.write('\n')

for texto in textos[1:]:
        st.markdown(f'##### {texto}')
st.caption('*Fonte: [UNFA - Fundo de População das Nações Unidas](https://brazil.unfpa.org/pt-br/preven%C3%A7%C3%A3o-da-gravidez-na-adolesc%C3%AAncia)*')
st.divider()

texto_dados = next((t for t in textos if 'Em 2024' in t), '')


# Pedi auxilio para IA, para extrair os números interessados no texto, para exibir no metrics
numeros = re.search(
    r'registrou ([\d.]+).*?e ([\d.]+) nascimentos',
    texto_dados
    )

if numeros:
    total_15_19_2024 = int(numeros.group(1).replace('.', ''))
    total_10_14_2024 = int(numeros.group(2).replace('.', ''))

    total_10_14_2023 = int(df['faixa_10_a_14'].sum())
    total_15_19_2023 = int(df['faixa_15_a_19'].sum())

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            'Nascimentos de mães de 10 a 14 anos — 2024',
            total_10_14_2024,
            delta=f'{((total_10_14_2024 - total_10_14_2023) / total_10_14_2023) * 100:.1f}% em relação aos casos de 2023',
            delta_color='inverse',
        )

    with col2:
        st.metric(
            'Nascimentos de mães de 15 a 19 anos — 2024',
            total_15_19_2024,
            delta=f'{((total_15_19_2024 - total_15_19_2023) / total_15_19_2023) * 100:.1f}% em relação aos casos de 2023',
            delta_color='inverse',
        )


titulos = [
    'Desafios da gravidez na adolescência no Brasil',
    'Impactos na economia brasileira',
]

for i, imagem in enumerate(imagens):
    if i < len(titulos):
        st.subheader(titulos[i])

    st.image(str(imagem))