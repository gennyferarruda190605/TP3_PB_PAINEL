from fastapi import FastAPI, Query
from typing import Literal
from src.data_access import obter_dados


app = FastAPI(title='API do Painel ODS 03 - Nascidos Vivos de Mães Adolescentes')

ufs = Literal[
    'Acre',
    'Alagoas',
    'Amapá',
    'Amazonas',
    'Bahia',
    'Ceará',
    'Distrito Federal',
    'Espírito Santo',
    'Goiás',
    'Maranhão',
    'Mato Grosso',
    'Mato Grosso do Sul',
    'Minas Gerais',
    'Pará',
    'Paraíba',
    'Paraná',
    'Pernambuco',
    'Piauí',
    'Rio de Janeiro',
    'Rio Grande do Norte',
    'Rio Grande do Sul',
    'Rondônia',
    'Roraima',
    'Santa Catarina',
    'São Paulo',
    'Sergipe',
    'Tocantins'
]

@app.get('/natalidade', tags=['natalidade'], summary='Lista todos os estados')
def listar_estados(limite: int = Query(43, ge=1, le=43, description='Quantas Ufs, no máximo.')):
    '''
    Devolve os dados de todos os estados: id, nome (uf) e nascidos vivos
    de mães de 10 a 14 anos e de 15 a 19 anos (2023).

    '''
    dados = obter_dados()
    lista = dados[:limite]

    return{'quantd_ufs': limite,
           'Fonte': 'Agregados do IBGE (SIDRA)',
            'dados': lista}


@app.get('/natalidade/{uf}', tags=['natalidade'], summary='Consultar um estado')
def consultar_estado(uf: ufs):
    '''
    Devolve os dados de um único estado escolhido pelo nome, o id e nascidos vivos
    de mães de 10 a 14 anos e de 15 a 19 anos (2023).

    Exemplos de uso: `/natalidade/Amazonas` · `/natalidade/São Paulo`
    '''
    dados = obter_dados()
    lista = [linha for linha in dados if linha['uf'] == uf]

    return {'Fonte': 'Agregados do IBGE (SIDRA)',
            'dados': lista}

