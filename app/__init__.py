"""
Anti-Fraud Document Analysis System
Sistema de análise de documentos com detecção de fraude usando Azure AI

Principais componentes:
- AntiFraudSystem: Sistema principal de orquestração
- DocumentService: Extração de texto via Azure Document Intelligence
- FraudAnalyzer: Análise de risco via Azure OpenAI
- AzureConfig: Configurações dos serviços Azure
- RiskThresholds: Limiares de classificação de risco

Exemplo de uso:
    >>> from app import AntiFraudSystem
    >>> system = AntiFraudSystem()
    >>> result = system.process_document("documento.pdf")
    >>> print(result['fraud_analysis']['risk_level'])
"""

# Metadados do pacote
__version__ = "1.0.0"
__author__ = "Azure AI Solutions Team"
__license__ = "MIT"
__email__ = "support@example.com"

# Imports principais para facilitar uso do pacote
from app.config import AzureConfig, RiskThresholds
from app.document_service import DocumentService
from app.fraud_analyzer import FraudAnalyzer
from app.main import AntiFraudSystem

# Define o que é exportado quando fazem "from app import *"
__all__ = [
    # Classes principais
    "AntiFraudSystem",
    "DocumentService", 
    "FraudAnalyzer",
    # Configuração
    "AzureConfig",
    "RiskThresholds",
    # Metadados
    "__version__",
    "__author__",
]
