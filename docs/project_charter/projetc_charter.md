# Project Charter - Painel de Natalidade entre Mães Adolescentes no Brasil

## 1. Contexto e problema de Négocio

#### A gravidez na adolescência é um problema de saúde pública com forte desigualdade regional no Brasil. Ela está associada a riscos obstétrico, abandono escolar e a prolongação de ciclos de vulnerabilidade socioeconômica. Gestores de saúde e educação carecem de uma visão consolidada, por UF, da quantidade de nascidos vivos de mães adolescentes para priorizar investimentos em saúde reprodutiva e educação sexual.

#### ***Pergunta afiada:***

Quais estados do Brasil, apresentam maior número (absoluto e relativo) de nascidos vivos de mães adolescentes (10 a 19 anos) em 2023, e devem ser priorizadas em políticas de saúde reprodutiva e educação sexual?

## 2. Objetivos e Metas

* **OBJETIVO GERAL** - Disponibilizar painel com valores absolutos de nascidos vivos por mães adolescentes na faixa de dois grupos, sendo 10 a 14 anos e 15 a 19 anos, por UF. A separação do grupo, é com intuito de dar atenção prioritária no grupo de 10 a 14 anos, que são faixas étarias consideradas mais 'perigosas e precárias', para natalidade.

* **METAS**:
   1. Mapear a distribuição do problema no país
   2. Localizar regiões e estados com mais casos
   3. Comparar quantidade de casos nos grupos de faixas étarias
   4. Visualizar quais são os impactos desse problema
   5. Contextualizar os dados numéricos com conteúdo textual sobre o tema, extraído de fonte jornalística especializada (SCP)
   6. Permitir que o próprio usuário complemente o painel com novos dados (texto ou numéricos), ampliando a análise sem depender de nova coleta
   7. Oferecer os dados para outros sistemas por meio de uma API, com métodos, GET E POST
   8. Apresentar texto, imagens e indicadores complementares do portal UNFPA
   9. Comparar os números dos casos de 2024 citados pela UNFPA com os totais de 2023 do IBGE
   10. Organizar o painel em páginas, cada uma respondendo a uma pergunta, com um menu de navegação

## 3. Indicadores de sucesso (KPIs)

| KPI | Como medimos | Meta |
| --- | --- | --- |
| Cobertura de dados | nº de UFs com dado carregado | 27/27 |
| Cobertura etária | nº de faixas etárias exibidas (10–14 e 15–19 anos) | 2/2 |
| Disponibilidade da fonte textual | notícia coletada e processada em frases | 1/1 |
| Complementação dos Dados | usuário consegue enviar CSV e ver os dados refletidos no painel (nuvem, estatísticas ou gráfico) | Sim |
|Rotas da API documentadas	| nº de rotas visíveis e descritas na página /docs | ≥ 2|
|Consistência painel | API	painel e API leem a mesma fonte, pela mesma função (obter_dados) | Sim
|Navegação do painel	| Todas as páginas do menu abrem sem erro | Sim |


## 4. ODS atendido e justificativa

* **ODS 3 — Saúde e Bem-Estar, meta 3.7 - garantir o acesso universal aos serviços de saúde sexual e reprodutiva.**

* Justificativa: O número de nascidos vivos de mães adolescentes é um indicador relevante de saúde sexual e reprodutiva. A gravidez na adolescência pode estar associada a desigualdades de gênero e a impactos na continuidade dos estudos, relacionando-se também aos ODS 4 (Educação de Qualidade), 8 (Trabalho Decente e Crescimento Econômico) e 1 (Erradicação da Pobreza). Por isso, analisar esse tema ajuda a compreender vulnerabilidades sociais e a orientar políticas públicas de saúde, educação e proteção social.

## 5. Público-alvo (stakeholders)

* Gestores públicos de saúde (secretarias estaduais/municipais de saúde, Ministério da Saúde).
* Gestores e formuladores de política educacional (educação sexual em escolas).
* Pesquisadores e ONGs que atuam em saúde reprodutiva e juventude.
* Sistemas e programas de terceiros que precisam consumir os dados diretamente, sem copiar planilhas ou raspar o painel.

## 6. Escopo

* **Dentro**: Coleta de dados via API de Agregados do IBGE (TABELA 8174), tratamento, visualização por UF; coleta de conteúdo textual via web scraping (Beautiful Soup) de notícia da Sociedade Catarinense de Pediatria (SCP) sobre gravidez na adolescência, com estatísticas básicas (contagem de palavras, vocabulário) e nuvem de palavras; serviço de upload de arquivos CSV para o usuário complementar os dados textuais ou numéricos exibidos; cache (`st.cache_data`) e estado de sessão (`st.session_state`) para performance e persistência das interações; filtros interativos (faixa etária, região, ordenação) via `st.form`.
* Painel em múltiplas páginas, com roteador (st.navigation) e menu lateral em seções.
* API em FastAPI, com rotas de consulta (GET) /natalidade e /natalidade/{uf}, documentadas na página /docs.
* Rota de envio de dados (POST)
* Download dos dados em tabelas em CSV pelo painel.


## 7. Fontes de dados previstas

* API de Agregados do IBGE (tabela 8174, variável 9433) — nascidos vivos de mães adolescentes por UF.
* Notícia do portal da Sociedade Catarinense de Pediatria (SCP), coletada via web scraping.
* Portal UNFPA — texto e imagens sobre gravidez na adolescência no Brasil, coletado via web scraping.
* Arquivos CSV enviado pelo usuário via upload na interface, como fonte complementar opcional.
* Detalhamento completo disponível em data_summary_report.md

## 8. Riscos e mitigação

| Risco | Mitigação |
| --- | --- |
| API do IBGE fora do ar ou instável | fallback para amostra em cache (data/sample/) |
| Mudança de formato/URL da API (versão v3 do SIDRA) | função de acesso isolada em src/ + testes |
| Site da SCP fora do ar, lento ou com mudança de layout | tentativas com timeout e novas requisições; arquivo `.txt` da última coleta bem-sucedida é mantido e reutilizado pelo app |
| Arquivo CSV enviado pelo usuário malformado, vazio ou com codificação diferente | leitura nunca levanta exceção — tenta `utf-8-sig`, `utf-8` e `latin-1`, e devolve mensagem de erro amigável em vez de quebrar o app |
| Cache compartilhado exibir dado de um usuário para outro | dado do upload nunca é cacheado com `st.cache_data` e fica guardado apenas por sessão em `st.session_state` |
| Painel usa dados da API (FastAPI)	| O painel é integrado com a API do FastAPI `comum.py : organizar_df()` , o FastAPI precisa de um servidor para funcionar, caso venha falhar, o painel usa o cachê |
|Filtros voltarem ao padrão quando o usuário troca de página	| `comum.py : preservar_filtros()` , executada pelo roteador antes de cada página


