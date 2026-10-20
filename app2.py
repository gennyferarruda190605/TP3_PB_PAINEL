import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from comum import inicializar_estado, preservar_filtros

inicializar_estado()
preservar_filtros()


st.set_page_config(page_title='Painel ODS 03 - BRASIL🩺💚', layout='wide')
st.title('ODS 03 - Painel de Monitoramento: Nascidos Vivos de Mães Adolescentes🤱📊')

st.divider()

pagina = st.navigation(
    {
        'Painel': [
            st.Page('paginas/inicio.py', title='Início', icon='🏠', default=True),
            st.Page('paginas/analise_ufs.py', title='Análise por UFs', icon='🗺️'),
            st.Page('paginas/analise_regioes.py', title='Análise por Regiões', icon='📊'),
        ],
        'Notícias': [
            st.Page('paginas/estatisticas.py', title='Estatísticas', icon='📰'),
            st.Page('paginas/uploader.py', title='Upload de CSV', icon='⬆️'),
        ],
        'Fonte dos Dados': [
                    st.Page('paginas/fonte_dados.py', title='Download de Dados', icon='⬇️'),
        ],

        'Sobre o projeto': [
            st.Page('paginas/sobre.py', title='Objetivos e metas', icon='🎯')
        ]
    }
)
pagina.run()