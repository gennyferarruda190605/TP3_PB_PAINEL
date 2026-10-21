'''
Análise de Dados CSV  — Via Uploader

Implementei uma função separada do bloco de aplicação do streamlit, para ler o arquivo csv, que foi enviado pelo usúario.
Um arquivo enviado por terceiros, pode não ser confiável, além de ter a possibilidade de ser realmente um csv. 
Tem 3 tipos de decodificação e devolve erro, caso não seja um csv ou tenha outros erros no arquivo.

Também uma função de mesclar frases, caso o arquivo csv, obtenha informações de textos.
'''


import csv
import io
import pandas as pd


def ler_csv(conteudo: bytes, sep: str = ',') -> tuple[pd.DataFrame | None, str]:

    if not conteudo:
        return None, 'O arquivo está vazio.'

    texto = None
    for codificacao in ('utf-8-sig', 'utf-8', 'latin-1'):
        try:
            texto = conteudo.decode(codificacao)
            break
        except UnicodeDecodeError:
            continue
    if texto is None:
        return None, 'Não consegui ler o arquivo como texto. Envie um arquivo CSV verdadeiro'

    try:
        df = pd.read_csv(io.StringIO(texto), sep=sep, engine='python')
    except (pd.errors.ParserError, pd.errors.EmptyDataError) as erro:
        return None, f'Não foi possível interpretar o CSV com o separador "{sep}": {erro}'

    if df.empty or df.shape[1] == 0:
        return None, 'O CSV não tem nenhuma coluna ou linha de dados.'

    return df, ''




def mesclar_frases(coletadas: list[str], enviadas: list[str]) -> pd.DataFrame:

    linhas = [{'frase': f, 'origem': 'coleta'} for f in coletadas]
    vistas = {f.strip().lower() for f in coletadas}

    for frase in enviadas:
        chave = frase.strip().lower()
        if chave in vistas:
            continue
        vistas.add(chave)
        linhas.append({'frase': frase, 'origem': 'enviado'})

    return pd.DataFrame(linhas)