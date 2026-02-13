Anti-Fraud Document Analysis com Azure AI

Projeto desenvolvido como desafio do curso de Inteligência Artificial da DIO.

Este projeto demonstra como utilizar serviços de IA da Azure para analisar documentos e identificar possíveis sinais de fraude a partir do conteúdo textual extraído.

Visão Geral

O sistema recebe um documento (PDF ou imagem), extrai o texto utilizando Azure Document Intelligence e realiza a análise de risco com Azure OpenAI.

A saída da análise inclui:

Score de risco (0.0 a 1.0)

Classificação de risco (Low, Medium, High)

Justificativa da análise

Elementos suspeitos identificados

Recomendações de ação

O objetivo é demonstrar a aplicação prática de modelos de linguagem para apoio à detecção de fraude documental.

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
└── README.md

Diretório app/

Contém a lógica principal do sistema:

main.py – Orquestra o fluxo completo de processamento.

config.py – Gerencia variáveis de ambiente e configurações.

document_service.py – Realiza a extração de texto via Azure.

fraud_analyzer.py – Executa a análise de fraude utilizando LLM.

Diretório docs/

Contém documentação complementar:

Arquitetura do sistema

Requisitos funcionais e não funcionais

Roadmap de evolução

Arquivo exemplos-prompt (1).md

Apresenta exemplos de prompts utilizados para estruturar a análise de fraude com o modelo.

Fluxo de Funcionamento

O usuário fornece um arquivo (PDF ou imagem).

O sistema envia o documento para o Azure Document Intelligence.

O texto extraído é enviado ao Azure OpenAI.

O modelo retorna uma análise estruturada em JSON.

O sistema classifica automaticamente o nível de risco.

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


O sistema exibirá o resultado no terminal e salvará automaticamente um arquivo JSON com a análise.

Exemplo de Saída
{
  "success": true,
  "fraud_analysis": {
    "risk_score": 0.72,
    "risk_level": "Medium",
    "justification": "Análise detalhada...",
    "suspicious_elements": [],
    "recommendations": [],
    "confidence": 0.85
  }
}

Limitações

Requer conexão ativa com a Azure.

O modelo fornece análise probabilística.

Não substitui revisão humana em casos críticos.

Possíveis Evoluções

Processamento em lote de documentos

Interface web

Validação automática de CPF/CNPJ

API REST para integração com outros sistemas
