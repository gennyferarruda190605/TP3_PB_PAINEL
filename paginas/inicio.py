import streamlit as st
from comum import carregar_df

df = carregar_df()


st.subheader('A gravidez na adolescência é um problema de saúde pública com forte desigualdade regional no Brasil.  \
 Ela está associada a riscos obstétricos, abandono escolar e à continuidade de ciclos de vulnerabilidade socioeconômica.')

st.subheader('Este painel reúne **dados oficiais do IBGE (SIDRA)** para mostrar, por UF e por região, quantos bebês nasceram de mães ' \
'de **10 a 14** e de **15 a 19 anos** em 2023 — alinhado ao **ODS 3** (Saúde e Bem-Estar) da Agenda 2030 e noticías coletadas do portal SCP.')

st.subheader('Foco Principal ')
st.info('##### Quais estados do Brasil, apresentam maior número (absoluto e relativo) de nascidos vivos de mães adolescentes (10 a 19 anos) \
em 2023, e devem ser priorizadas em políticas de saúde reprodutiva e educação sexual?')


st.divider()
st.subheader('O que cada página responde')

st.page_link('paginas/analise_ufs.py', label='Análise de UFs', icon='🗺️')
st.caption('Distribuição dos casos por UFs com filtros')

st.page_link('paginas/analise_regioes.py', label='Análise de Regiões', icon='📊')
st.caption('Distribuição dos casos por região, com filtro para regiões e grupos de idade' )

st.page_link('paginas/estatisticas.py', label='Estatísticas', icon='📰')
st.caption('Notícia sobre o tema, em números e em nuvem palavras')

st.page_link('paginas/uploader.py', label='Uploader de CSV', icon='⬆️')
st.caption('Carregar seu arquivo CSV para análise e mesclar com os dados atuais.')

st.page_link('paginas/fonte_dados.py', label='Download de Dados', icon='⬇️')
st.caption('Fontes dos Dados do painel e download.')

st.page_link('paginas/sobre.py', label='Objetivo e metas', icon='🎯')
st.caption('Explicação completa problema de negocio e metas a serem cumpridas.')


st.markdown('### Para saber mais')
st.markdown(
    '- [Conecta Brasil — ODS](https://conectabrasil.org/ods)\n'
    '- [Tabela SIDRA 8174 — indicador 3.7.2](https://sidra.ibge.gov.br/tabela/8174)\n'
    '- [Documentação da API de Agregados do IBGE](https://servicodados.ibge.gov.br/api/docs/agregados?versao=3)'
)

st.caption('Fonte dos indicadores: API de Dados Agregados do IBGE (SIDRA), 2023.')
