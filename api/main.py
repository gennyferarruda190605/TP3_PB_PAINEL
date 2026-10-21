from fastapi import FastAPI, Query, status
from typing import Literal
from pydantic import BaseModel, Field
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


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Script para o método POST, baseado no ensino do professor Thiago 

 
class NovaObservacao(BaseModel):
    uf: ufs
    texto: str = Field(
        min_length=5,
        max_length=500,
        description='Observação enviada pelo usuário sobre a UF.',
    )


class Observacao(NovaObservacao):
    id: int


observacoes: list[Observacao] = []

@app.post('/observacoes', response_model=Observacao, status_code=status.HTTP_201_CREATED, tags=['observações'], summary='Enviar uma observação', description='Recebe uma observação associada a uma UF.' \
    ''' Exemplo de envio: {
        'uf': 'Amazonas',
        'texto': 'Ampliar as ações de prevenção para adolescentes'.
        }''',
    )


def criar_observacao(nova_observacao: NovaObservacao):
    registro = Observacao(
        id=len(observacoes) + 1,
        **nova_observacao.model_dump(),
    )
    observacoes.append(registro)
    return registro



@app.get('/observacoes', response_model=list[Observacao], tags=['observações'], summary='Listar observações', description='Devolve as observações enviadas durante a execução da API.')
def listar_observacoes():
    return observacoes


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Scripts para uso do GET, com Endpoints (caminho) e consultas (parâmetros)

@app.get('/')
def inicio():
    return {
        'mensagem': 'API do Painel ODS 03 - Gravidez na adolescência',
        'documentacao': 'http://127.0.0.1:8000/docs',
        'dados': 'http://127.0.0.1:8000/natalidade'
    }



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

