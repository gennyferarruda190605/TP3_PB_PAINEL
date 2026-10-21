'''
Coleta de notícias sobre gravidez na adolescência.

Utilização de Beautiful Soup para ler a página SCP(Sociedade Catarinense de Pediatria), salva os dados em TXT.
Funções de limpeza, transformação, salvar arquivo e entregar os dados'''

from pathlib import Path
import requests
from bs4 import BeautifulSoup
import re

BASE = Path(__file__).resolve().parent.parent
ARQUIVO_TEXTO = BASE / 'data' / 'processed' / 'noticias_gravidez_adolescente.txt'

URL = ('https://www.scp.org.br/gravidez-na-adolescencia-um-desafio-de-saude-publica-que-exige-o-olhar-atento-da-pediatria/')

UA = {'User-Agent': 'INFNET_GENNYFER_PB'}


def coletar_noticias() -> list[dict]:

    resposta = requests.get(URL, headers=UA, timeout=30, verify=False)
    resposta.raise_for_status()

    sopa = BeautifulSoup(resposta.text, 'html.parser')

    conteudo = sopa.find('div', attrs={'data-elementor-type': 'single-post'})

    textos = []
    for tag in conteudo.find_all('p'):
        texto = tag.get_text(strip=True)
        textos.append(texto)
    return '\n\n'.join(textos)

def dividir_frases(texto: str) -> list[str]:
    return [f.strip() for f in re.split(r'\.(?=\s|$)', texto) if f.strip()]

def salvar_txt(texto: str) -> None:
    frases = dividir_frases(texto)
    ARQUIVO_TEXTO.parent.mkdir(parents=True, exist_ok=True)
    ARQUIVO_TEXTO.write_text('\n'.join(frases), encoding='utf-8')

def obter_frases() -> list[str]:
    with open(ARQUIVO_TEXTO, encoding='utf-8') as textos:
        return textos.read().splitlines()


if __name__ == '__main__':
    paragrafos = coletar_noticias()
    salvar_txt(paragrafos)
    print(f'TXT salvo em: {ARQUIVO_TEXTO}')

