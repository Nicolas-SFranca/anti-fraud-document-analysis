# Arquitetura do Sistema

## Visão Geral

O sistema Anti-Fraud Document Analysis foi projetado seguindo os princípios de Clean Architecture e separação de responsabilidades. A arquitetura é composta por camadas bem definidas que facilitam manutenção, testabilidade e evolução.

## Princípios Arquiteturais

### 1. Separação de Responsabilidades
Cada módulo tem uma responsabilidade clara e única:
- `config.py`: Gerenciamento de configurações
- `document_service.py`: Extração de texto
- `fraud_analyzer.py`: Análise de risco
- `main.py`: Orquestração

### 2. Inversão de Dependências
As camadas superiores não dependem de implementações concretas, mas de abstrações. Isso permite fácil substituição de serviços.

### 3. Design for Testability
Cada componente pode ser testado isoladamente através de injeção de dependências.

## Componentes Principais

### Config Layer (config.py)

Responsabilidade: Gerenciar todas as configurações do sistema.

**Classes:**

- `AzureConfig`: Armazena credenciais e endpoints dos serviços Azure
  - Carrega variáveis de ambiente
  - Valida configurações obrigatórias
  - Fornece configurações centralizadas

- `RiskThresholds`: Define limiares de classificação de risco
  - `low_max`: 0.3
  - `medium_max`: 0.7
  - `high_min`: 0.8

**Decisões de Design:**
- Uso de dataclasses para imutabilidade e clareza
- Validação centralizada de variáveis de ambiente
- Separação de configurações de negócio (thresholds) e infraestrutura (Azure)

### Document Service Layer (document_service.py)

Responsabilidade: Abstrair a complexidade de extração de texto.

**Classe Principal:**

`DocumentService`
- Inicialização com credenciais Azure
- Suporte a múltiplas fontes (arquivo local, URL)
- Cálculo de confiança da extração
- Tratamento de erros robusto

**Métodos:**

1. `extract_text_from_file(file_path)`
   - Processa arquivo local
   - Retorna texto + metadados
   - Calcula confiança média

2. `extract_text_from_url(document_url)`
   - Processa documento remoto
   - Mesma estrutura de resposta

3. `_calculate_average_confidence(result)`
   - Método privado
   - Calcula média de confiança por palavra

**Decisões de Design:**
- Uso do cliente Azure Document Intelligence prebuilt-document
- Retorno padronizado com estrutura success/error
- Logging detalhado de cada etapa
- Extração de metadados úteis para análise posterior

### Fraud Analyzer Layer (fraud_analyzer.py)

Responsabilidade: Análise de risco usando inteligência artificial.

**Classe Principal:**

`FraudAnalyzer`
- Integração com Azure OpenAI
- Prompts especializados em detecção de fraude
- Validação de formato de resposta
- Classificação automática de risco

**Métodos:**

1. `analyze_fraud_risk(document_text, metadata)`
   - Constrói prompts contextualizados
   - Faz chamada ao modelo LLM
   - Valida e classifica resultado

2. `_build_system_prompt()`
   - Define o comportamento do modelo
   - Especifica formato JSON de saída
   - Lista critérios de análise

3. `_build_user_prompt(document_text, metadata)`
   - Combina texto e metadados
   - Formata para melhor análise

4. `validate_analysis_format(analysis)`
   - Valida campos obrigatórios
   - Verifica ranges de valores

**Decisões de Design:**
- Temperatura baixa (0.2) para respostas mais determinísticas
- Uso de response_format JSON para garantir saída estruturada
- Sistema de prompts com instruções explícitas
- Separação entre construção de prompt e execução

### Orchestration Layer (main.py)

Responsabilidade: Coordenar o fluxo completo de processamento.

**Classe Principal:**

`AntiFraudSystem`
- Inicialização de todos os serviços
- Orquestração do pipeline completo
- Gestão de erros em diferentes estágios
- Persistência de resultados

**Fluxo de Processamento:**

```
1. Carregar configurações (.env)
2. Inicializar serviços (Document + OpenAI)
3. Extrair texto do documento
4. Analisar risco de fraude
5. Consolidar resultado
6. Retornar estrutura padronizada
```

**Decisões de Design:**
- Padrão fail-fast com logging detalhado
- Resultado indica em qual stage ocorreu erro
- Separação de processamento local vs URL
- Interface de linha de comando simples

## Fluxo de Dados

```
[Entrada: Documento]
        │
        ▼
[DocumentService.extract_text_from_file]
        │
        ├─► Success: {text, metadata}
        └─► Failure: {error, success: false}
        │
        ▼
[FraudAnalyzer.analyze_fraud_risk]
        │
        ├─► Sistema Prompt (especialista)
        ├─► User Prompt (texto + metadata)
        ├─► Azure OpenAI (GPT-4)
        │
        ▼
[JSON Response]
        │
        ├─► risk_score (0.0-1.0)
        ├─► justification
        ├─► suspicious_elements []
        ├─► recommendations []
        └─► confidence
        │
        ▼
[RiskThresholds.classify_risk]
        │
        ├─► Low (0.0-0.3)
        ├─► Medium (0.4-0.7)
        └─► High (0.8-1.0)
        │
        ▼
[Resultado Consolidado]
```

## Decisões Técnicas Importantes

### 1. Por que Azure Document Intelligence?

- OCR de alta qualidade
- Suporte nativo a múltiplos formatos
- Extração de estrutura e layout
- API simples e bem documentada
- Já disponível no ecossistema Azure

### 2. Por que Azure OpenAI?

- Conformidade e segurança de dados (LGPD/GDPR)
- Modelos GPT-4 de última geração
- Integração nativa com ambiente Azure
- SLA empresarial
- Sem compartilhamento de dados para treinamento

### 3. Por que Response Format JSON?

- Garante saída estruturada
- Evita parsing de markdown ou texto livre
- Facilita validação
- Reduz erros de integração
- Melhora consistência

### 4. Por que Dataclasses?

- Imutabilidade (frozen=True opcional)
- Type hints nativos
- Menos boilerplate que classes normais
- Integração com mypy
- Serialização fácil

### 5. Por que Logging Estruturado?

- Rastreabilidade de operações
- Debugging em produção
- Métricas e observabilidade
- Auditoria de processos

## Padrões Utilizados

### 1. Dependency Injection
Configurações injetadas nos serviços via construtor.

### 2. Factory Method
`AzureConfig.from_environment()` cria instância a partir do ambiente.

### 3. Template Method
Fluxo de processamento define estrutura, steps podem variar.

### 4. Strategy Pattern
Análise de risco pode ser substituída por outras estratégias.

## Segurança

### 1. Gestão de Credenciais
- Uso de variáveis de ambiente
- Nunca hardcode de secrets
- Validação na inicialização

### 2. Validação de Input
- Verificação de arquivos existentes
- Validação de formato de resposta
- Tratamento de exceções

### 3. Logging Seguro
- Não loga credenciais
- Não loga conteúdo completo de documentos
- Apenas metadados e sumários

## Escalabilidade

### Limitações Atuais
- Processamento síncrono
- Um documento por vez
- Sem paralelização

### Melhorias Futuras
- Processamento assíncrono (asyncio)
- Fila de documentos
- Processamento em batch
- Cache de resultados
- Rate limiting inteligente

## Testabilidade

### Unit Tests Possíveis
- `RiskThresholds.classify_risk()`: testa classificação
- `AzureConfig.from_environment()`: testa validação
- `FraudAnalyzer._build_system_prompt()`: testa prompt
- `DocumentService._calculate_average_confidence()`: testa cálculo

### Integration Tests Possíveis
- Extração de documento exemplo
- Análise end-to-end
- Validação de formato de saída

### Mock Necessários
- Azure SDK clients
- Variáveis de ambiente
- Responses da API

## Observabilidade

### Métricas Importantes
- Tempo de extração de texto
- Tempo de análise de fraude
- Taxa de sucesso/falha
- Distribuição de risk scores
- Confiança média das extrações

### Logs Estruturados
- Início/fim de operações
- Erros com contexto
- Metadata de documentos processados

## Conformidade

### LGPD/GDPR
- Dados processados em região específica (Azure)
- Sem retenção de dados de treinamento
- Logs não contêm PII

### SOC 2
- Auditabilidade via logs
- Rastreabilidade de operações
- Segregação de responsabilidades

## Diagramas

### Diagrama de Sequência

```
User -> Main: process_document(file)
Main -> DocService: extract_text(file)
DocService -> Azure DI: analyze_document
Azure DI -> DocService: result
DocService -> Main: {text, metadata}
Main -> FraudAnalyzer: analyze_fraud(text)
FraudAnalyzer -> Azure OpenAI: completion
Azure OpenAI -> FraudAnalyzer: json_response
FraudAnalyzer -> Main: {risk_score, elements}
Main -> User: final_result
```

### Diagrama de Componentes

```
┌──────────────────────────────────┐
│       AntiFraudSystem            │
│  (Orchestration)                 │
└────┬─────────────────────────┬───┘
     │                         │
     ▼                         ▼
┌────────────────┐    ┌────────────────┐
│ DocumentService│    │ FraudAnalyzer  │
└────┬───────────┘    └────┬───────────┘
     │                     │
     ▼                     ▼
┌─────────────┐      ┌──────────────┐
│  Azure DI   │      │ Azure OpenAI │
└─────────────┘      └──────────────┘
```

## Conclusão

A arquitetura foi projetada para ser:
- Simples de entender
- Fácil de manter
- Testável
- Escalável
- Segura

Cada decisão foi tomada pensando em equilibrar simplicidade com robustez, permitindo que o sistema seja usado em produção enquanto mantém a clareza de código necessária para evolução futura.
