import streamlit as st


st.header('**Problema de Négocio📌🔍**')
st.markdown('##### A gravidez na adolescência é um problema de saúde pública com forte desigualdade regional no Brasil.  \
Ela está associada a riscos obstétrico, abandono escolar e a prolongação de ciclos de vulnerabilidade socioeconômica.  \
Gestores de saúde e educação carecem de uma visão consolidada, por UF, da quantidade de nascidos vivos de mães adolescentes para priorizar investimentos em saúde reprodutiva e educação sexual.')

st.subheader('Pergunta Chave🔖')
st.markdown('##### Quais estados do Brasil, apresentam maior número (absoluto e relativo) de nascidos vivos de mães adolescentes (10 a 19 anos) em 2023, e devem ser priorizadas em políticas de saúde reprodutiva e educação sexual?')

st.divider()

st.header('**Objetivo principal🎯**')
st.markdown('#### Disponibilizar painel com valores absolutos de nascidos vivos por mães adolescentes na faixa étaria, com o primeiro grupo sendo 10 a 14 anos e segundo grupo sendo 15 a 19 anos, por UF.')

st.subheader('Metas: ')
st.write(' * Com a separação dos grupos de faixas étarias, podemos ter uma atenção prioritária no grupo de 10 a 14 anos, que são faixas étarias consideradas mais 'perigosas e precárias' para natalidade.')
st.write(' * Visualizar as UF com maiores casos, para priorizar os investimentos em saúde e educação sexual.')

st.divider()

st.header('Links para mais informações da ODS 03 - Brasil 🔗🌐')
st.markdown(
    '- [Conecta Brasil — ODS](https://conectabrasil.org/ods)\n'
    '- [Tabela SIDRA 8174 — indicador 3.7.2](https://sidra.ibge.gov.br/tabela/8174)\n'
    '- [Documentação da API de Agregados do IBGE](https://servicodados.ibge.gov.br/api/docs/agregados?versao=3)'
)

st.caption('Fonte dos indicadores: API de Dados Agregados do IBGE (SIDRA), 2023.')