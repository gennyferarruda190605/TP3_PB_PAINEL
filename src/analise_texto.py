'''
Estatísticas básicas e Geração de Nuvens do texto coletado — Via Web Scraping.

Funções de limpezas das palavras, com intuito de facilicar no uso das funções de estatísticas (principalmente na função de contagens, para não separar a 
as mesmas palavras, pelo fato de uma ser maiusculas, outras minusculas, caracteres especiais e outros) e geração das nuvens de palavras.
'''

import re
import unicodedata
from collections import Counter
from pathlib import Path
from wordcloud import WordCloud

from src.data_access2 import ARQUIVO_TEXTO

stop_words = frozenset('''
a as o os um uma uns umas de do da dos das em no na nos nas por para per com sem sob sobre
ao aos à às e ou mas que se quando onde como qual quais quanto quantos porque pois
ele ela eles elas eu tu nos vos me te lhe lhes seu sua seus suas meu minha dele dela
este esta estes estas esse essa esses essas isso isto aquele aquela aquilo
ser sao é foi era sera seja sendo estar esta estao estava ter tem tinha havia ha
mais menos muito muitos pouco pouca todo toda todos todas outro outra outros outras
ja nao sim tambem entre ate apos antes durante desde cada mesmo mesma assim ainda
segundo disse afirmou destacou ressaltou explicou acordo caso ano anos dia dias
pelo pela pelos pelas pode podem podera deve devem havera fica ficam vai vao
grande grandes parte partes forma vezes apenas cerca ainda entao logo
'''.split())

minimo = 4


def carregar_texto(caminho: Path = ARQUIVO_TEXTO) -> str:
    return caminho.read_text(encoding='utf-8') if caminho.exists() else ''


def _sem_acento(palavra: str) -> str:
    decomposta = unicodedata.normalize('NFD', palavra.lower())
    return ''.join(c for c in decomposta if unicodedata.category(c) != 'Mn')


def palavras(texto: str) -> list[str]:
    return re.findall(r'\w+(?:-\w+)?', texto.lower(), flags=re.UNICODE)


def frequencia(texto: str, quantidade: int = 15) -> list[dict]:
    contagem = Counter(
        palavra
        for palavra in palavras(texto)
        if len(palavra) >= minimo
        and not palavra.isdigit()
        and _sem_acento(palavra) not in stop_words
    )
    return [
        {'palavra': palavra, 'ocorrencias': vezes}
        for palavra, vezes in contagem.most_common(quantidade)
    ]


def estatisticas(texto: str) -> dict:
    todas = palavras(texto)
    uteis = [p for p in todas if len(p) >= minimo and _sem_acento(p) not in stop_words]
    return {
        'caracteres': len(texto),
        'palavras': len(todas),
        'palavras_uteis': len(uteis),
        'vocabulario': len(set(uteis)),
    }


def gerar_nuvem(texto: str, stopwords: set | None = None):

    return WordCloud(
        stopwords=stopwords or set(),
        width=800,
        height=400,
        background_color='white',
        max_words=150,
    ).generate(texto)


if __name__ == '__main__':
    texto = carregar_texto()
    print('estatísticas:', estatisticas(texto))