Anti-Fraud Document Analysis com Azure AI

Projeto desenvolvido como desafio do curso de IA da DIO.

O objetivo é analisar documentos (PDF ou imagem), extrair o texto usando serviços de IA da Azure e aplicar um modelo de linguagem para identificar possíveis sinais de fraude.

Objetivo do Projeto

Criar um sistema simples que:

Recebe um documento.

Extrai o texto utilizando Azure Document Intelligence.

Analisa o conteúdo com Azure OpenAI.

Retorna:

Score de risco (0.0 a 1.0)

Classificação (Low, Medium, High)

Justificativa

Elementos suspeitos

Recomendações

O foco é demonstrar o uso prático de serviços de IA para apoiar processos de detecção de fraude documental.

Tecnologias Utilizadas

Python 3.8+

Azure Document Intelligence (OCR)

Azure OpenAI Service

python-dotenv

Azure SDK

Estrutura do Projeto
anti-fraud-document-analysis/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── document_service.py
│   └── fraud_analyzer.py
├── docs/
│   ├── arquitetura.md
│   ├── requisitos.md
│   └── roadmap.md
├── exemplos-prompt (1).md
├── requirements (1).txt
└── README

app/

Contém a lógica principal do sistema:

main.py – Orquestra o fluxo completo.

config.py – Carrega variáveis de ambiente.

document_service.py – Responsável pela extração de texto.

fraud_analyzer.py – Responsável pela análise de fraude usando LLM.

docs/

Documentação complementar:

Arquitetura do sistema.

Requisitos funcionais e não funcionais.

Roadmap de evolução.

exemplos-prompt (1).md

Exemplos de prompts utilizados para orientar o modelo na análise de fraude.

Como Funciona o Fluxo

O usuário fornece um arquivo (PDF ou imagem).

O sistema envia o documento para o Azure Document Intelligence.

O texto extraído é enviado para o Azure OpenAI.

O modelo retorna uma análise estruturada em JSON.

O sistema classifica o risco com base no score retornado.

Configuração

Crie um arquivo .env na raiz do projeto com as seguintes variáveis:

AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=
AZURE_DOCUMENT_INTELLIGENCE_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_KEY=
AZURE_OPENAI_DEPLOYMENT_NAME=

Instalação

Clone o repositório:

git clone <url-do-repositorio>
cd anti-fraud-document-analysis


Instale as dependências:

pip install -r "requirements (1).txt"

Execução

Para analisar um documento local:

python app/main.py caminho/do/documento.pdf


O sistema exibirá o resultado no terminal e salvará um arquivo JSON com a análise.

Exemplo de Saída

O sistema retorna um JSON estruturado como:

{
  "success": true,
  "fraud_analysis": {
    "risk_score": 0.72,
    "risk_level": "Medium",
    "justification": "...",
    "suspicious_elements": [],
    "recommendations": [],
    "confidence": 0.85
  }
}

Limitações

Dependente de conexão com a Azure.

Não substitui análise humana.

O score é probabilístico, baseado em modelo de linguagem.

Possíveis Evoluções

Processamento em lote.

Interface web.

Validação automática de CPF/CNPJ.

API REST.
