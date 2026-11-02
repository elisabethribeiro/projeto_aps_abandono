# Clinical Decision-Support System: Gestão de Linhas de Cuidado e Mitigação de Falso Abandono em APS

## Visão Geral do Projeto

Na Atenção Primária à Saúde (APS) e na Saúde Populacional, o acompanhamento de condições crônicas (como Hipertensão Arterial Sistêmica, Diabetes Mellitus e Dislipidemia) depende da continuidade do cuidado. Um dos principais desafios operacionais em programas de saúde preventiva é a identificação errônea de falso abandono: pacientes rotulados como inativos ou desvinculados do programa de acompanhamento, mas que mantêm consultas ativas com o Médico de Família e Comunidade (MFC) para queixas pontuais ou renovação de receitas.

Essa falha de fluxo gera impactos críticos:
- Desassistência Clínica: Pacientes crônicos perdem rastreios periódicos de complicações e exames laboratoriais essenciais.
- Inconsistência de Indicadores: Métricas populacionais e metas de acreditação de qualidade apresentam taxas de adesão defasadas.
- Inércia Operacional: A equipe multiprofissional não aproveita a presença física do paciente na unidade para realizar a reativação da linha de cuidado.

Este projeto entrega uma solução de ponta a ponta: desde o processamento e modelagem dos dados em Python até a implementação de uma ferramenta de suporte à decisão clínica no ponto de cuidado via Google Apps Script.

## Arquitetura da Solução

1. Camada Analítica (Python / Pandas / Faker): Geração de base populacional 100% sintética, simulação de parâmetros de contato clínico e aplicação de regras lógicas para identificar discrepâncias entre o cadastro da linha de cuidado e os agendamentos reais.
2. Camada Visual (Matplotlib): Produção de gráficos analíticos com anotação numérica direta para priorização de linhas de maior evasão e análise percentual de abandono.
3. Camada Operacional (Google Sheets + Apps Script): Automação executada via menu superior personalizado (onOpen) que varre a agenda do dia, cruza os identificadores com a base de pendências usando estrutura em memória (Map) e insere o status assistencial diretamente no fluxo de trabalho da equipe.

## Principais Resultados e Métricas

Na simulação analítica realizada com uma população de 1.000 vidas:
- Identificação precisa de 119 pacientes em situação de falso abandono (última consulta presencial há menos de 90 dias, porém com cadastro inativo na Linha de Cuidado).
- Linhas com maior necessidade de reativação imediata destacadas para foco prioritário da equipe multiprofissional.
- Redução do tempo de checagem do histórico do paciente de minutos de busca manual no prontuário para execução em bloco de menos de 1 segundo na abertura da agenda.

## Tecnologias e Metodologias

- Linguagem Principal: Python 3.10+
- Manipulação de Dados: Pandas, NumPy
- Geração de Dados Sintéticos: Faker (com seed fixada para garantia de reprodutibilidade estrita)
- Visualização de Dados: Matplotlib
- Automação e Integração Cloud: Google Apps Script (JavaScript moderno, V8 runtime), Google Sheets API
- Arquitetura de Dados: Otimização de busca em memória via estruturas chave-valor (Map) com leitura e gravação em lote (getDataRange().getValues() / setValues()).

## Estrutura do Repositório

```
├── data/
│   ├── pendencias_gerais.csv         # Tabela de referência clínica sintética
│   └── agenda.csv                    # Simulação de agenda diária de consultas
├── notebooks/
│   └── pipeline_analise_populacional.py  # Tratamento, regras e gráficos
├── scripts/
│   └── automacao_agenda.js           # Código Google Apps Script para a agenda
├── README.md                         # Documentação executiva do projeto
└── requirements.txt                  # Dependências do projeto Python
```

## Como Executar o Projeto

### 1. Ambiente Python (Processamento e Gráficos)
Instale as dependências:
```bash
pip install -r requirements.txt
```
Execute o script em `notebooks/pipeline_analise_populacional.py` para processar a base sintética e gerar os dados.

### 2. Ambiente Google Sheets (Ferramenta de Suporte à Decisão)
1. Crie uma planilha com duas abas: `pendencias_gerais` e `agenda`.
2. Importe os arquivos CSV correspondentes disponibilizados na pasta `data/`.
3. Acesse Extensões > Apps Script e cole o código contido em `scripts/automacao_agenda.js`.
4. Salve e recarregue a planilha.
5. Utilize o menu superior Ações Clínicas > Atualizar Status LC para processar a agenda.

## Conformidade Ética e Proteção de Dados (LGPD)

Este projeto foi desenvolvido estritamente com dados sintéticos gerados programmaticamente através da biblioteca Faker em ambiente de desenvolvimento pessoal isolado. Nenhum dado de saúde individual, identificador pessoal real, prontuário físico/eletrônico ou informação proprietária institucional foi utilizado ou exposto, em total conformidade com a Lei Geral de Proteção de Dados Pessoais (Lei nº 13.709/2018 - LGPD).
