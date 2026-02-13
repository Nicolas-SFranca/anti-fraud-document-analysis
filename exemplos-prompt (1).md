# Exemplo de Prompt e Resposta

Este documento demonstra como funciona a interação com o Azure OpenAI para análise de fraude.

## System Prompt

O system prompt define o comportamento e especialização do modelo:

```
Você é um especialista em detecção de fraudes em documentos.

Sua tarefa é analisar documentos e identificar potenciais sinais de fraude.

Você deve responder APENAS com um objeto JSON válido seguindo esta estrutura:

{
    "risk_score": float entre 0.0 e 1.0,
    "justification": "Explicação detalhada da análise",
    "suspicious_elements": [
        "Lista de elementos suspeitos encontrados"
    ],
    "recommendations": [
        "Lista de recomendações"
    ],
    "confidence": float entre 0.0 e 1.0
}

Critérios de análise:
- Inconsistências em datas
- Informações contraditórias
- Padrões incomuns de formatação
- CNPJ/CPF com problemas
- Valores ou quantidades suspeitas
- Assinaturas ou carimbos irregulares
- Qualidade da digitalização

Não inclua nenhum texto fora do JSON.
```

## User Prompt - Exemplo 1: Nota Fiscal Suspeita

### Input do Documento

```
NOTA FISCAL ELETRÔNICA
NF-e: 12345678901234567890123456789012345678901234

EMITENTE:
Razão Social: EMPRESA FICTICIA LTDA
CNPJ: 12.345.678/0001-90
Endereço: Rua das Flores, 123 - São Paulo/SP

DESTINATÁRIO:
Nome: João da Silva
CPF: 123.456.789-00
Endereço: Av. Principal, 456 - Rio de Janeiro/RJ

DATA DE EMISSÃO: 15/02/2025
DATA DE SAÍDA: 10/02/2025

PRODUTOS:
- Notebook Dell: R$ 15.000,00
- Mouse Logitech: R$ 50,00

VALOR TOTAL: R$ 15.050,00

Assinatura Digital: Presente
```

### Resposta Esperada

```json
{
  "risk_score": 0.85,
  "justification": "O documento apresenta múltiplos sinais de fraude graves. A principal inconsistência é a data de saída (10/02/2025) anterior à data de emissão (15/02/2025), o que é logicamente impossível. O CNPJ 12.345.678/0001-90 possui um padrão sequencial típico de dados fictícios. O valor do notebook (R$ 15.000,00) está significativamente acima do preço de mercado para equipamentos desse tipo. Além disso, a combinação de um valor alto de produto com um item de baixo valor (mouse de R$ 50) é um padrão comum em fraudes de nota fiscal.",
  "suspicious_elements": [
    "Data de saída (10/02/2025) anterior à data de emissão (15/02/2025)",
    "CNPJ com padrão sequencial suspeito (12.345.678/0001-90)",
    "Valor do notebook muito acima do mercado (R$ 15.000,00)",
    "CPF com padrão numérico sequencial (123.456.789-00)",
    "Combinação suspeita de produto de alto valor com item irrelevante"
  ],
  "recommendations": [
    "Validar CNPJ junto à Receita Federal",
    "Verificar autenticidade da nota fiscal no portal SEFAZ",
    "Solicitar comprovante de pagamento",
    "Verificar histórico de transações do emitente",
    "Confirmar identidade do destinatário",
    "Bloquear transação até verificação completa"
  ],
  "confidence": 0.92
}
```

---

## User Prompt - Exemplo 2: Contrato Legítimo

### Input do Documento

```
CONTRATO DE PRESTAÇÃO DE SERVIÇOS

Pelo presente instrumento particular, as partes:

CONTRATANTE:
XYZ Tecnologia S.A.
CNPJ: 00.123.456/0001-78
Endereço: Av. Paulista, 1000 - São Paulo/SP

CONTRATADA:
ABC Consultoria Empresarial Ltda.
CNPJ: 98.765.432/0001-12
Endereço: Rua Comercial, 200 - São Paulo/SP

Têm entre si justo e contratado o seguinte:

CLÁUSULA PRIMEIRA - DO OBJETO
Prestação de serviços de consultoria em gestão empresarial.

CLÁUSULA SEGUNDA - DO VALOR
R$ 10.000,00 (dez mil reais) mensais.

CLÁUSULA TERCEIRA - DA VIGÊNCIA
12 meses a partir de 01/03/2026.

São Paulo, 13 de fevereiro de 2026.

_____________________________        _____________________________
XYZ Tecnologia S.A.                  ABC Consultoria Empresarial Ltda.
```

### Resposta Esperada

```json
{
  "risk_score": 0.15,
  "justification": "O documento apresenta características de um contrato legítimo. As informações estão consistentes e bem estruturadas. Os CNPJs possuem formato válido sem padrões sequenciais óbvios. O valor mensal de R$ 10.000,00 está dentro da faixa razoável para serviços de consultoria empresarial. A data de vigência (01/03/2026) é posterior à data de assinatura (13/02/2026), o que é apropriado. O endereço da Av. Paulista é uma localização comum e legítima para empresas em São Paulo. As cláusulas são claras e seguem padrões contratuais normais.",
  "suspicious_elements": [
    "Nenhum elemento suspeito significativo identificado"
  ],
  "recommendations": [
    "Validar CNPJs junto à Receita Federal como procedimento padrão",
    "Verificar se as empresas estão ativas e regulares",
    "Confirmar poderes de representação dos signatários",
    "Arquivar contrato em sistema de gestão documental"
  ],
  "confidence": 0.88
}
```

---

## User Prompt - Exemplo 3: Documento com Inconsistências Moderadas

### Input do Documento

```
RECIBO DE PAGAMENTO

Recebi de: CONSTRUÇÕES XYZ LTDA
CNPJ: 12.345.678/0001-99

A quantia de: R$ 8.500,00 (oito mil e quinhentos reais)

Referente a: Serviços de pintura

Data: 13/02/2026
Local: São Paulo

___________________________
João Pereira da Silva
CPF: 987.654.321-00
```

### Resposta Esperada

```json
{
  "risk_score": 0.45,
  "justification": "O documento apresenta alguns elementos que requerem atenção, mas não são definitivamente fraudulentos. O CNPJ possui um final sequencial (0001-99) que pode ser legítimo mas merece validação. O recibo é relativamente simples e falta informações detalhadas sobre os serviços prestados (área pintada, tipo de tinta, período de execução). O valor de R$ 8.500,00 está em uma faixa razoável para serviços de pintura, mas sem detalhamento é difícil validar. O documento não possui testemunhas ou elementos adicionais de validação. A descrição genérica 'Serviços de pintura' sem especificações é comum tanto em documentos legítimos quanto fraudulentos.",
  "suspicious_elements": [
    "CNPJ com final sequencial que requer validação",
    "Falta de especificação detalhada dos serviços prestados",
    "Ausência de testemunhas ou elementos de validação adicional",
    "Descrição genérica sem menção a endereço do serviço",
    "Recibo manuscrito sem numeração ou controle"
  ],
  "recommendations": [
    "Validar CNPJ da empresa contratante na Receita Federal",
    "Solicitar nota fiscal complementar ao recibo",
    "Verificar se há contrato de prestação de serviços anterior",
    "Confirmar identidade e CPF do prestador de serviços",
    "Solicitar fotos ou evidências do serviço realizado",
    "Verificar histórico de pagamentos similares"
  ],
  "confidence": 0.75
}
```

---

## Padrões de Risco por Score

| Risk Score | Risk Level | Descrição | Ação Recomendada |
|------------|------------|-----------|------------------|
| 0.0 - 0.3 | Low | Documento apresenta características normais com poucos ou nenhum indicador de fraude | Processamento normal com validações básicas |
| 0.4 - 0.7 | Medium | Documento possui elementos que requerem atenção e verificação adicional | Análise manual recomendada antes de aprovação |
| 0.8 - 1.0 | High | Documento apresenta múltiplos sinais graves de fraude | Rejeição imediata ou investigação aprofundada obrigatória |

---

## Elementos Comuns em Documentos Fraudulentos

### 1. Inconsistências Temporais
- Datas de emissão posteriores a datas de vencimento
- Datas futuras em documentos históricos
- Sequência temporal impossível de eventos

### 2. Dados Sequenciais ou Padrões Óbvios
- CPF: 111.111.111-11, 123.456.789-00
- CNPJ: 12.345.678/0001-90
- Números de telefone: (11) 11111-1111

### 3. Valores Anormais
- Valores muito acima ou abaixo do mercado
- Valores redondos em contextos que deveriam ter centavos
- Discrepâncias entre valor por extenso e numérico

### 4. Formatação Inconsistente
- Mistura de fontes ou estilos
- Alinhamentos irregulares
- Qualidade variável de digitalização em partes do documento

### 5. Informações Contraditórias
- Endereços incompatíveis com CEPs
- Estados diferentes em campos relacionados
- Nomes de empresas divergentes em partes do documento

### 6. Ausência de Elementos Esperados
- Falta de assinaturas ou carimbos
- Ausência de números de controle
- Falta de informações obrigatórias por lei

---

## Configuração de Temperatura

A temperatura usada no modelo é **0.2** para garantir:

- Respostas mais determinísticas
- Menor variabilidade em análises similares
- Foco em padrões factuais ao invés de criativos
- Maior consistência entre execuções

Para casos que requeiram análise mais exploratória, a temperatura pode ser ajustada para 0.3-0.4.

---

## Validação da Resposta

Todo JSON retornado deve passar pelas seguintes validações:

```python
def validate_response(response):
    required_fields = [
        "risk_score",
        "justification",
        "suspicious_elements",
        "recommendations"
    ]
    
    # Verifica campos obrigatórios
    for field in required_fields:
        if field not in response:
            return False
    
    # Valida risk_score
    if not (0.0 <= response["risk_score"] <= 1.0):
        return False
    
    # Valida tipos
    if not isinstance(response["suspicious_elements"], list):
        return False
    
    if not isinstance(response["recommendations"], list):
        return False
    
    return True
```

---

## Métricas de Qualidade da Análise

### Confiança (Confidence)

O campo `confidence` indica o quão confiante o modelo está em sua análise:

- **0.9 - 1.0**: Alta confiança - elementos claros e inequívocos
- **0.7 - 0.9**: Confiança moderada - análise sólida mas com alguma ambiguidade
- **< 0.7**: Baixa confiança - documento ambíguo ou falta de informações

### Score de Risco (Risk Score)

Calculado baseado em:
- Número de elementos suspeitos identificados
- Gravidade de cada elemento
- Contexto do tipo de documento
- Padrões conhecidos de fraude

A fórmula exata é proprietária do modelo LLM, mas pode ser influenciada através de prompt engineering.
