# Documento de Requisitos

## 1. Introdução

### 1.1 Propósito
Este documento descreve os requisitos funcionais e não-funcionais do sistema Anti-Fraud Document Analysis, uma solução para detecção automatizada de fraudes em documentos utilizando serviços de inteligência artificial do Azure.

### 1.2 Escopo
O sistema processa documentos digitais (PDF e imagens), extrai texto através de OCR avançado e analisa o conteúdo em busca de indicadores de fraude, fornecendo um score de risco e recomendações.

### 1.3 Definições
- **Document Intelligence**: Serviço Azure de extração de texto via OCR
- **Azure OpenAI**: Serviço de modelos de linguagem grandes (LLM)
- **Risk Score**: Valor numérico de 0.0 a 1.0 indicando probabilidade de fraude
- **Risk Level**: Classificação categórica (Low, Medium, High)

## 2. Requisitos Funcionais

### RF01 - Extração de Texto de Documentos

**Descrição**: O sistema deve extrair texto de documentos PDF e imagens.

**Prioridade**: Alta

**Critérios de Aceitação**:
- Aceitar formatos: PDF, PNG, JPG, JPEG
- Extrair texto com confiança mínima de 70%
- Processar documentos de até 500 MB
- Retornar texto completo e metadados (páginas, idioma, confiança)

**Entradas**:
- Arquivo local (caminho do sistema)
- URL de documento (opcional)

**Saídas**:
```json
{
  "success": true,
  "text": "Texto extraído...",
  "metadata": {
    "page_count": 3,
    "language": "pt-BR",
    "confidence": 0.95
  }
}
```

### RF02 - Análise de Risco de Fraude

**Descrição**: O sistema deve analisar o texto extraído e identificar sinais de fraude.

**Prioridade**: Alta

**Critérios de Aceitação**:
- Gerar score numérico entre 0.0 e 1.0
- Classificar em níveis: Low, Medium, High
- Listar elementos suspeitos específicos
- Fornecer justificativa detalhada
- Incluir recomendações de ação

**Entradas**:
- Texto do documento
- Metadados de extração (opcional)

**Saídas**:
```json
{
  "risk_score": 0.72,
  "risk_level": "Medium",
  "justification": "Texto explicativo...",
  "suspicious_elements": ["Item 1", "Item 2"],
  "recommendations": ["Ação 1", "Ação 2"],
  "confidence": 0.85
}
```

### RF03 - Classificação Automática de Risco

**Descrição**: O sistema deve classificar automaticamente o nível de risco baseado no score.

**Prioridade**: Média

**Critérios de Aceitação**:
- Score 0.0-0.3: Low
- Score 0.4-0.7: Medium
- Score 0.8-1.0: High
- Classificação imediata após análise

### RF04 - Processamento por Linha de Comando

**Descrição**: O sistema deve permitir processamento via CLI.

**Prioridade**: Média

**Critérios de Aceitação**:
- Aceitar arquivo como argumento
- Exibir resultado no console
- Salvar resultado em arquivo JSON
- Retornar código de saída apropriado (0=sucesso, 1=erro)

**Exemplo de Uso**:
```bash
python app/main.py documento.pdf
```

### RF05 - Interface Programática

**Descrição**: O sistema deve fornecer API Python para integração.

**Prioridade**: Alta

**Critérios de Aceitação**:
- Classe `AntiFraudSystem` instanciável
- Método `process_document(file_path)` público
- Método `process_document_url(url)` público
- Método `save_result(result, path)` público

**Exemplo de Uso**:
```python
system = AntiFraudSystem()
result = system.process_document("doc.pdf")
```

### RF06 - Validação de Configuração

**Descrição**: O sistema deve validar configurações na inicialização.

**Prioridade**: Alta

**Critérios de Aceitação**:
- Verificar existência de variáveis de ambiente obrigatórias
- Lançar exceção descritiva se faltarem credenciais
- Validar formato de endpoints Azure

### RF07 - Tratamento de Erros

**Descrição**: O sistema deve tratar erros em cada etapa do processamento.

**Prioridade**: Alta

**Critérios de Aceitação**:
- Capturar erros de extração
- Capturar erros de análise
- Retornar estrutura indicando stage do erro
- Incluir mensagem de erro clara

**Estrutura de Erro**:
```json
{
  "success": false,
  "stage": "extraction",
  "error": "Mensagem de erro",
  "file": "documento.pdf"
}
```

## 3. Requisitos Não-Funcionais

### RNF01 - Performance

**Descrição**: O sistema deve processar documentos em tempo razoável.

**Critérios**:
- Extração: máximo 30 segundos por página
- Análise: máximo 15 segundos
- Total: máximo 2 minutos para documento de 10 páginas

### RNF02 - Confiabilidade

**Descrição**: O sistema deve ser confiável e resiliente.

**Critérios**:
- Taxa de sucesso mínima: 95%
- Retry automático em caso de falhas temporárias (até 3 tentativas)
- Timeout configurável (padrão: 120 segundos)

### RNF03 - Segurança

**Descrição**: O sistema deve manter segurança de dados e credenciais.

**Critérios**:
- Credenciais apenas em variáveis de ambiente
- Não logar conteúdo sensível de documentos
- Não armazenar documentos processados
- Comunicação HTTPS com APIs Azure

### RNF04 - Manutenibilidade

**Descrição**: O código deve ser fácil de manter e entender.

**Critérios**:
- Código seguindo PEP 8
- Docstrings em todas as funções públicas
- Type hints em parâmetros e retornos
- Separação clara de responsabilidades
- Logging estruturado

### RNF05 - Escalabilidade

**Descrição**: O sistema deve suportar crescimento futuro.

**Critérios**:
- Arquitetura permitir processamento assíncrono
- Suporte a múltiplas instâncias paralelas
- Configurações externalizadas
- Sem dependências de estado local

### RNF06 - Observabilidade

**Descrição**: O sistema deve permitir monitoramento e debugging.

**Critérios**:
- Logging em dois níveis: console e arquivo
- Logs incluem timestamp, nível e contexto
- Métricas de tempo de processamento
- Rastreabilidade de operações

### RNF07 - Compatibilidade

**Descrição**: O sistema deve ser compatível com ambientes padrão.

**Critérios**:
- Python 3.8+
- Linux, Windows, macOS
- Dependências via pip/requirements.txt
- Sem dependências de sistema externas

### RNF08 - Usabilidade

**Descrição**: O sistema deve ser fácil de usar.

**Critérios**:
- Instalação em 3 passos (clone, pip install, configurar .env)
- Mensagens de erro claras
- Documentação completa em README
- Exemplos de uso fornecidos

## 4. Requisitos de Dados

### RD01 - Formato de Entrada

**Tipos Aceitos**:
- PDF (até versão 2.0)
- PNG
- JPG/JPEG
- TIFF

**Tamanho Máximo**: 500 MB

**Requisitos de Qualidade**:
- Resolução mínima: 150 DPI
- Texto legível (não manuscrito)

### RD02 - Formato de Saída

**Tipo**: JSON estruturado

**Campos Obrigatórios**:
- success (boolean)
- fraud_analysis.risk_score (float)
- fraud_analysis.risk_level (string)
- fraud_analysis.justification (string)
- fraud_analysis.suspicious_elements (array)

**Encoding**: UTF-8

## 5. Requisitos de Integração

### RI01 - Azure Document Intelligence

**Versão da API**: 2023-07-31 ou superior

**Modelo Utilizado**: prebuilt-document

**Autenticação**: API Key via header

### RI02 - Azure OpenAI

**Versão da API**: 2024-02-15-preview ou superior

**Modelo Recomendado**: GPT-4

**Parâmetros**:
- Temperature: 0.2
- Max tokens: 1000
- Response format: JSON object

## 6. Requisitos de Qualidade

### RQ01 - Acurácia da Extração

**Métrica**: Confiança média acima de 85%

**Critério**: Calculado sobre todas as linhas extraídas

### RQ02 - Consistência da Análise

**Métrica**: Mesma entrada produz mesma classificação de risco

**Tolerância**: Variação de ±0.05 no score

### RQ03 - Validação de Saída

**Critério**: 100% das análises bem-sucedidas devem ter formato JSON válido

**Campos Obrigatórios**: Todos presentes e com tipos corretos

## 7. Casos de Uso

### UC01 - Análise de Nota Fiscal

**Ator**: Analista de Compliance

**Fluxo**:
1. Usuário fornece PDF da nota fiscal
2. Sistema extrai texto
3. Sistema analisa indicadores de fraude (CNPJ, datas, valores)
4. Sistema retorna score e elementos suspeitos
5. Usuário revisa resultado e toma ação

### UC02 - Análise em Lote (Futuro)

**Ator**: Sistema Automatizado

**Fluxo**:
1. Sistema recebe lista de documentos
2. Processa cada documento sequencialmente
3. Consolida resultados
4. Gera relatório agregado

### UC03 - Integração com Pipeline

**Ator**: Desenvolvedor

**Fluxo**:
1. Desenvolvedor importa `AntiFraudSystem`
2. Instancia classe no código
3. Processa documentos programaticamente
4. Integra resultados no sistema existente

## 8. Restrições

### Restrições Técnicas
- Requer conectividade com Azure (sem modo offline)
- Dependente de quotas da Azure
- Limitado por rate limits das APIs

### Restrições de Negócio
- Custos por processamento (pay-per-use)
- Idiomas otimizados: português e inglês
- Não substitui revisão humana em casos críticos

### Restrições Legais
- Conformidade com LGPD/GDPR
- Dados não podem ser usados para treinamento
- Retenção de logs conforme política de privacidade

## 9. Premissas

- Azure Document Intelligence está disponível
- Azure OpenAI tem modelo GPT-4 deployado
- Usuário possui credenciais válidas
- Documentos são em idiomas suportados pelo OCR
- Internet estável disponível

## 10. Dependências Externas

### Serviços Azure
- Azure Document Intelligence
- Azure OpenAI Service

### Bibliotecas Python
- azure-ai-formrecognizer
- openai (Azure SDK)
- python-dotenv

## 11. Critérios de Aceitação do Sistema

O sistema será considerado aceito quando:

1. Processar com sucesso 95% dos documentos de teste
2. Classificar corretamente 90% dos casos conhecidos de fraude
3. Executar em menos de 2 minutos para documentos padrão (até 10 páginas)
4. Documentação completa e compreensível
5. Testes de integração passando
6. Zero hardcoded secrets no código
