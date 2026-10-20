''' 
Coleta via API do IBGE em Python com biblioteca Requests  

Busca a lista de estados e os dados de nascidos vivos de mães adolescentes, 
salvando um cache local para caso a API cair e não parar o app. '''

import json
from pathlib import Path
import requests

# Pedi ajuda ao Claude para salvar os arquivos na pasta data
BASE = Path(__file__).resolve().parent.parent
ARQUIVO_RAW = BASE / 'data' / 'raw' / 'natalidade_bruto.json'
ARQUIVO_PROCESSED = BASE / 'data' / 'processed' / 'natalidade_limpo.json'
ARQUIVO_SAMPLE = BASE / 'data' / 'sample' / 'natalidade_cache.json'

UA = {'User-Agent': 'INFNET_GENNYFER_PB'}

URL = (
    'https://servicodados.ibge.gov.br/api/v3/agregados/8174/periodos/2023'
    '/variaveis/9433?localidades=N3[all]&classificacao=58[1142,1143]'
)
faixa_etaria = {'1142': '10 a 14 anos', '1143': '15 a 19 anos'}


def _coletar_dados_api(timeout: int = 30) -> list:
    
    try:
        import urllib3
        urllib3.disable_warnings()
    except Exception:
        pass
    
    resposta = requests.get(URL, headers=UA, timeout=timeout, verify=False)
    resposta.raise_for_status()
    
    return resposta.json()


def _processar_dados(dados_brutos: list) -> list[dict]:
    dados_agrupados = {}
    
    for resultado in dados_brutos[0]['resultados']:
        
        codigo_faixa = list(resultado['classificacoes'][0]['categoria'].keys())[0]
        
        if codigo_faixa == '1142':
            coluna_faixa = 'faixa_10_a_14'
        elif codigo_faixa == '1143':
            coluna_faixa = 'faixa_15_a_19'

        for serie in resultado['series']:
            id_uf = int(serie['localidade']['id'])  
            uf = serie['localidade']['nome']
            valor = serie['serie'].get('2023')
            qtd_nascidos = int(valor) if valor and valor.isdigit() else 0
            
            if uf not in dados_agrupados:
                dados_agrupados[uf] = {
                    'id': id_uf,
                    'uf': uf,
                    'faixa_10_a_14': 0,
                    'faixa_15_a_19': 0
                }
            
            dados_agrupados[uf][coluna_faixa] = qtd_nascidos
            
    return list(dados_agrupados.values())


def obter_dados() -> list[dict]:
    
    try:

    # Apesar de parecer/ser um pouco desnecessário, salvar todos esses arquivos, pretendi seguir a estrutura padrão, para ter uma melhor experiência sobre.

        # Copia dos dados brutos em json coletados da API, na pasta data/raw
        dados_brutos = _coletar_dados_api()
        ARQUIVO_RAW.parent.mkdir(parents=True, exist_ok=True)
        ARQUIVO_RAW.write_text(json.dumps(dados_brutos, ensure_ascii=False, indent=2), encoding='utf-8')

        # Copia dos dados processados e limpos na pasta data/processed
        dados_limpos = _processar_dados(dados_brutos)
        ARQUIVO_PROCESSED.parent.mkdir(parents=True, exist_ok=True)
        ARQUIVO_PROCESSED.write_text(json.dumps(dados_limpos, ensure_ascii=False, indent=2), encoding='utf-8')

        # Salvando dados processados na pasta data/sample, para uso cache, caso API venha cair.
        ARQUIVO_SAMPLE.parent.mkdir(parents=True, exist_ok=True)
        ARQUIVO_SAMPLE.write_text(json.dumps(dados_limpos, ensure_ascii=False, indent=2), encoding='utf-8') # Coloquei todos os dados limpos, porque não é um arquivo muito grande, ao contrário, eu colocaria somente uma amostra
        
        return dados_limpos
        
    except Exception as erro:
        print(f'Erro na API ({erro}). Carregando cache local...')
        
        if ARQUIVO_PROCESSED.exists():
            return json.loads(ARQUIVO_SAMPLE.read_text(encoding='utf-8'))
            
        print('Nenhum arquivo cache encontrado para uso.')
        return []


if __name__ == '__main__':
    dados = obter_dados()
    if dados:
        print(f'Sucesso! {len(dados)} registros processados e salvos.')
