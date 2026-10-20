# Data Summary Report  - Painel de Natalidade entre Mães Adolescentes no Brasil

## Fonte de Dados - API

| FONTE | TIPO | ENDPOINT | OBJETIVO | 
| --- | --- | --- | --- |
| Agregados do IBGE (SIDRA) | JSON via API | https://servicodados.ibge.gov.br/api/v3/agregados/8174/periodos/2023/variaveis/9433?localidades=N3[all]&classificacao=58[1142,1143] | 27 UFs, grupos de idades, quantidade de casos |

* **PARÂMETROS** : 
* agregados/8174: Tabela 8174 (Número de nascidos vivos de mães adolescentes por 1.000 mulheres).
* periodos/2023: Dados referente ao ano de 2023
* variaveis/9433: A métrica principal solicitada pela tabela (o valor específico de nascimentos).
* localidades=N3[all] (todas as UFs)
* classificacao=58: O parâmetro 58 isola a dimensão 'Grupos de Idade':
  * 1142: Mães de 10 a 14 anos.
  * 1143: Mães de 15 a 19 anos.


## Fonte de Dados -  Web Scpraing

| ITEM | VALOR |
| ---  | --- |
| Fonte | Portal SCP - https://www.scp.org.br/gravidez-na-adolescencia-um-desafio-de-saude-publi++ca-que-exige-o-olhar-atento-da-pediatria/ |
| Seções | Home - Noticias 2026 |
| Tipo | HTML (Não estruturado - Legível para humanos) |
| Coleta | Localizado na pasta src/data_access2.py |
| Saída | Localizado na pasta data/processed/noticias_gravidez_adolescente.txt |

### **Observações - Robots.TXT** 

Não fiz inserção de leitura do robots.txt com urllib.robotparser, pois consultei na web e não havia impedindo para web scraping em nenhum endpoint da página.

Resposta do ROBOTS.TXT:

START YOAST BLOCK
User-agent: *

Disallow:


### **Observações - Licença** 

Procurei a página sobre a licença e termos, porém, não encontrei, então entrei em contato com os responsavéis, para pedir a permissão do uso dos dados da notícia.
Foi retornado que estava apta para usar os dados no projeto, porém, com a condição de citação da fonte, no projeto.


## Fonte de Dados - CSV (Via uploader do Streamlit)

Para leitura dos dados csv, é chamada a função na pasta src/analise_csv_uploader. 
No app do Streamlit, temos a função de mesclar os dados (também na pasta src/analise_csv_uploader).
Como não tenho a informação de qual dado será acrescentado na página, para dados textuais temos a opção de visualizar e mesclar os dados, e para dados númericos, inclui a opção de gráfico para visualização.

| ITEM | VALOR |
| ---  | --- |
| Origem | CSV enviado pelo próprio usuário via st.file_uploader |
| Tipo | Estruturado (CSV), entrada NÃO CONFIÁVEL |
| Validação | src/analise_csv_uploader:: ler_csv() — devolve (linhas, erro) |
| Codificações aceitas | utf-8-sig - utf-8 - latin-1 (dentro da função ler_csv()) |
| Procedência | Os dados enviados, recebem a identificação de 'enviada' |

# Estrutura Inicial - Dados API

A função de coletar dados da API do IBGE (localizada na pasta src/data_access.py), retorna os dados na estrutura JSON(semi-estruturados).

Variável (nome)| Tipo | Objetivo
--- | --- | --- |
classificacoes.nome|String|Nome da categoria analisada (Grupo de idade)
classificacoes.categoria|Dicionário|Código numérico que indica o grupo da faixa étaria
series|Lista (Array)|Lista que armazena os dados estatísticos detalhados de cada localidade.
localidade.id|String|Número oficial de identificação da UF (Fornecido pelo IBGE)
localidade.nivel.id|String|Código interno que define o nível territorial do dado
localidade.nivel.nome|String|Descrição por extenso do nível geográfico (Unidade da Federação)
localidade.nome|String|Nome  da UF 
serie|Dicionário|Estrutura chave-valor que armazena o ano e o seu respectivo dado.
serie.'2023'|String|Quantidade de casos daquela categoria no ano referenciado.

# Estrutura final - Dados API

Após a coleta pela função de coleta, os dados passam pela função processar dados, onde é retornado em uma lista de dicionários, as variáveis principais a serem usadas, em seguinda transformando as variáveis, o id das UF , e a responsável pela quantidade de nascidos, de string para inteiro.
No arquivo app.py, importo os dados com as variáveis necessárias retornada pela função obter_dados, e transformo em DataFrame, para aplicação no Streamlit.

| Variável (nome) | Tipo | Objetivo |
| --- | --- | --- |
| id | Inteiro | Número oficial de identificação da UF (Fornecido pelo IBGE) |
| uf | String | Nome da UF |
| faixa_10_a_14 | Inteiro | Quantidade de casos da faixa étaria (10 a 14 anos) |
| faixa_15_a_19 | Inteiro| Quantidade de casos da faixa étaria (15 a 19 anos)  |


# Estrutura final - Dados WebScraping

| Coluna | Tipo | Objetivo |
| --- | --- | --- |
|  0 | String | Frases da notícia |

**Qualidade e observações:**
* Conteúdo jornalístico, público e sob licença aberta; sem dado pessoal (LGPD n/a).
* A estrutura da página é escolha do dono do site e pode mudar sem aviso — (esse é o motivo da coleta estar separada do app do streamlit).
* Caso a estrutura mude e o seletor quebrar, o painel continua no ar com os dados salvos da última coleta.


# Estrutura final - CSV (Via uploader)

Não há como definir especifícamente, mas será devolvido um DataFrame.

**Observações:**
* Fontes enviadas por terceiros, não são confiáveis.

# Objetivo 

Optei nesse projeto, limitar os dados no ano de 2023, com intuito de podermos analisar e visualizar a distribuição com os dados mais recentes fornecidos. Escolhi soemnte essas 4 variáveis para a análise no Streamlit, pois, cheguei a uma conclusão que outras variáveis não ofereciam informações úteis para a pesquisa.
Os dados via API, nos dá informações concretas para análise explorátoria dos casos de fato.
Os dados via web scraping, oferece informações visando os principais pautas que se dão pelo 'problema atual' e uma visão mais ampla sobre o assunto.
Dados via uploader pelo usuário, completa ambos.
