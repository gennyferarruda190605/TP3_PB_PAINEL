from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser


URL = 'https://brazil.unfpa.org/pt-br/prevenção-da-gravidez-na-adolescência'
UA = {'User-Agent': 'INFNET_GENNYFER_PB'}


BASE = Path(__file__).resolve().parent.parent
ARQUIVO_IMAGENS = BASE / 'data' / 'processed' / 'imagens'
ARQUIVO_TEXTO = (BASE / 'data' / 'processed' / 'texto_unfpa.txt')


rp = RobotFileParser()
resposta_robots = requests.get('https://brazil.unfpa.org/robots.txt')
rp.parse(resposta_robots.text.splitlines())


def coletar_imagem():

    permitido = rp.can_fetch('*', URL)

    if permitido:

        resposta = requests.get(URL, headers=UA, timeout=30)
        resposta.raise_for_status()

        sopa = BeautifulSoup(resposta.text, 'html.parser')

        # Pedi auxilio da IA, para conseguir coletar essas imagens, pois estavam tendo dificuldades para "mostrar o caminho exato" das imagens, para coleta
        imagens = sopa.select(
        'img[src*="gravidez-adolescencia-1-panorama"], '
        'img[data-src*="gravidez-adolescencia-1-panorama"], '
        'img[src*="gravidez-adolescencia-2-economia"], '
        'img[data-src*="gravidez-adolescencia-2-economia"]'
        )

        ARQUIVO_IMAGENS.mkdir(parents=True, exist_ok=True)
        imagens_salvas = []

        for imagem in imagens:
            endereco = imagem.get('src') or imagem.get('data-src')
            if not endereco:
                continue

            url_imagem = urljoin(URL, endereco)
            resposta_imagem = requests.get(url_imagem, headers=UA, timeout=30)
            resposta_imagem.raise_for_status()

            nome_arquivo = url_imagem.rsplit('/', 1)[-1]
            arquivo = ARQUIVO_IMAGENS / nome_arquivo
            arquivo.write_bytes(resposta_imagem.content)

            imagens_salvas.append(arquivo)
            print(f'Imagem salva em: {arquivo}')

        return imagens_salvas



def obter_imagens():

    if not ARQUIVO_IMAGENS.exists():
        return []

    return sorted(ARQUIVO_IMAGENS.glob('gravidez-adolescencia-*.png'))




def coletar_texto():

    permitido = rp.can_fetch('*', URL) 

    if permitido:

        resposta = requests.get(URL, headers=UA, timeout=30)
        resposta.raise_for_status()

        sopa = BeautifulSoup(resposta.text, 'html.parser')

        lista_alvo = None

        for lista in sopa.find_all('ul'):
            itens = lista.find_all('li', recursive=False)

            if any(
                'Em 2024, o Brasil registrou' in item.get_text(' ', strip=True)
                for item in itens
            ):
                lista_alvo = lista
                break

        if lista_alvo is None:
            raise ValueError('Não encontrei a lista de dados na página.')

        textos = ['Os números por trás da realidade']

        for item in lista_alvo.find_all('li', recursive=False):
            texto = item.get_text(' ', strip=True)
            if texto:
                textos.append(texto)

        return '\n'.join(textos)


def salvar_texto(texto: str):
    ARQUIVO_TEXTO.parent.mkdir(parents=True, exist_ok=True)
    ARQUIVO_TEXTO.write_text(texto, encoding='utf-8')


def obter_texto():
    if not ARQUIVO_TEXTO.exists():
        return []

    return ARQUIVO_TEXTO.read_text(encoding='utf-8').splitlines()



if __name__ == '__main__':
    texto = coletar_texto()
    salvar_texto(texto)
    print(f'Texto salvo em: {ARQUIVO_TEXTO}')