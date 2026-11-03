# Sistema de Mitigação de Falsos Abandonos no Manejo de Condições Crônicas na APS (Saúde Suplementar)

## Visão Geral do Projeto

Na Atenção Primária à Saúde (APS) o acompanhamento de condições crônicas (como Hipertensão Arterial Sistêmica, Diabetes Mellitus e Dislipidemia) fundamenta-se no atributo da longitudinalidade e na garantia da continuidade do cuidado ao longo do tempo. Um dos principais desafios operacionais em programas de saúde preventiva é a identificação errônea de falso abandono (ou falsas perdas de seguimento): pacientes rotulados como inativos ou desvinculados do programa de acompanhamento, mas que mantêm consultas ativas com a equipe.

Principais impactos dessa falha:
- Oportunidades de cuidado perdidas: O usuário vai até o serviço, mas a equipe não aproveita o momento para checar exames de rotina ou reavaliar sua condição de saúde.
- Indicadores incorretos: Os relatórios mostram falsas taxas de abandono e adesão defasada.
- Falha de informação: Falta de integração entre agendas e base de dados que impede o profissional de visualizar rapidamente se o paciente está ativo ou não nas linhas de cuidado.

Este projeto entrega uma solução de ponta a ponta:desde a análise e limpeza de dados com Python até um alerta simples na agenda de atendimento usando Google Planilhas e Apps Script.


## Arquitetura da Solução

```
[Google Colab] 
  ├── Criação de base sintética de pacientes (Faker / NumPy com seed 42)
  ├── Cruzamento de dados para achar falsos abandonos (Pandas)
  └── Visualização da análise (Matplotlib)
       │
       ▼ (Exportação das bases / Tabelas operacionais)
[Google Sheets]
  ├── Aba 'pendencias_gerais' (Base populacional)
  └── Aba 'agenda' (Lista de atendimentos do dia)
       │
       ▼
[Google Apps Script]
  └── Gatilho onOpen() ──► Menu customizado "Ações Clínicas"
                            └── Indexação em memória (Map O(1))
                            └── Gravação em lote na coluna 'Status LC'
```

1. **Camada Analítica e de Modelagem (Google Colab / Python)**:
   - Geração de base populacional 100% sintética com semente determinística.
   - Cruzamento de dados de última consulta para identificar falso abandono (pacientes classificados como inativos na linha, porém com atendimento nos últimos 90 dias).
   - Análise gráfica para identificação das linhas mais impactadas.
2. **Camada Operacional (Google Sheets)**:
   - Centralização dos dados populacionais na aba `pendencias_gerais`.
   - Simulação da lista de trabalho da equipe médica na aba `agenda`.
3. **Camada de Automação e Suporte à Decisão (Google Apps Script)**:
   - Criação de menu dinâmico no cabeçalho da planilha (`onOpen`).
   - Algoritmo otimizado com tabela hash (`Map()`) para validação em lote dos pacientes agendados.
   - Retorno em tempo real do status assistencial (`Pendente`, `Abandono`, `Em dia`) diretamente na agenda, alertando o médico antes do atendimento.
4. **Camada de Inteligência Artificial e Recomendações (Google GenAI / Gemini)**: Agente de IA (`APSRiskAdvisorAgentGoogle`) integrado via API que analisa os indicadores consolidados de absenteísmo e elabora automaticamente um relatório com planos de ação práticos e prioridades estratégicas para os gestores da unidade.
---

## Principais Resultados

Na simulação analítica executada sobre a coorte sintética de 1.000 vidas:
- Identificação precisa de **119 pacientes em falso abandono** (último contato presencial $\le$ 90 dias com status cadastral inativo).
- Mapeamento das linhas prioritárias para intervenção imediata da equipe.
- Tempo de resposta da automação no Google Sheets inferior a 1 segundo para a varredura e preenchimento de toda a agenda do turno.

---

## Ferramentas Utilizadas

- Python (Colab): Pandas, NumPy e Faker (para geração de dados sintéticos).
- Visualização: Matplotlib.
- Planilhas e Automação: Google Sheets e Google Apps Script (JavaScript).
- Inteligência Artificial Generativa: Google GenAI SDK, Google Gemini API (`gemini-2.5-flash`)
---

## Estrutura do Repositório

```
├── data/
│   ├── pendencias_gerais.csv         # Dados populacionais simulados
│   └── agenda.csv                    # Simulação de agenda diária do ambulatório
├── notebooks/
│   └── pipeline_analise_populacional.py  # Script executável no Google Colab
├── reports/
│   └── relatorio_recomendacoes_ia.md # Plano de ação estratégico gerado por IA
├── scripts/
│   └── automacao_agenda.js           # Código executado no Google Apps Script
├── README.md                         # Documentação do projeto
└── requirements.txt                  # Dependências para reprodução local/Colab
```

---

## Como Reproduzir o Projeto

### 1. Etapa de Dados e Análise (Google Colab)
1. Abra um novo notebook no [Google Colab](https://colab.research.google.com/).
2. Instale as dependências caso necessário:
   ```bash
   pip install pandas numpy matplotlib faker openpyxl
   ```
3. Execute o script `pipeline_analise_populacional.py` para gerar as bases populacionais e os arquivos `.csv` (ou `.xlsx`).

### 2. Etapa Operacional e Suporte à Decisão (Google Sheets + Apps Script)
1. No Google Planilhas, crie uma planilha nova.
2. Crie duas abas: `pendencias_gerais` e `agenda`.
3. Popule cada aba com os dados correspondentes gerados no Colab.
4. No menu superior da planilha, acesse **Extensões** > **Apps Script**.
5. Cole o código de `scripts/automacao_agenda.js` e salve.
6. Atualize a página do Google Planilhas (`F5`).
7. Acesse o menu **Ações Clínicas** > **Atualizar Status LC** para executar a classificação dos pacientes agendados.

### 3. Agente de Recomendações Estratégicas com IA
Para gerar o plano de ação analítico via IA:
1. Configure a variável de ambiente com a sua chave: `export GEMINI_API_KEY="sua_chave"` (ou configure nos secrets do Colab).
2. Execute o script:
   ```bash
   python scripts/agente_recomendacoes_ia.py
---

## Conformidade Ética e Proteção de Dados (LGPD)

Este projeto foi construído a partir de **dados fictícios gerados computacionalmente** no Google Colab, sem vínculo com prontuários reais, bases de pacientes ou sistemas corporativos. O estudo respeita integralmente as diretrizes da Lei Geral de Proteção de Dados Pessoais (Lei nº 13.709/2018 - LGPD) e os preceitos éticos de sigilo profissional.
