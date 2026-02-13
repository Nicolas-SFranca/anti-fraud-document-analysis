"""
Configuração do Sistema Anti-Fraude
Gerencia variáveis de ambiente e configurações centralizadas
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class AzureConfig:
    """Configurações dos serviços Azure"""
    
    # Document Intelligence
    document_intelligence_endpoint: str
    document_intelligence_key: str
    
    # Azure OpenAI
    openai_endpoint: str
    openai_key: str
    openai_deployment_name: str
    openai_api_version: str = "2024-02-15-preview"
    
    # Configurações de análise
    max_retry_attempts: int = 3
    timeout_seconds: int = 120
    
    @classmethod
    def from_environment(cls) -> 'AzureConfig':
        """Carrega configurações das variáveis de ambiente"""
        
        doc_endpoint = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT')
        doc_key = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY')
        openai_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        openai_key = os.getenv('AZURE_OPENAI_KEY')
        openai_deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')
        
        if not all([doc_endpoint, doc_key, openai_endpoint, openai_key, openai_deployment]):
            raise ValueError(
                "Variáveis de ambiente obrigatórias não configuradas. "
                "Verifique o arquivo .env.example"
            )
        
        return cls(
            document_intelligence_endpoint=doc_endpoint,
            document_intelligence_key=doc_key,
            openai_endpoint=openai_endpoint,
            openai_key=openai_key,
            openai_deployment_name=openai_deployment,
            openai_api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview'),
            max_retry_attempts=int(os.getenv('MAX_RETRY_ATTEMPTS', '3')),
            timeout_seconds=int(os.getenv('TIMEOUT_SECONDS', '120'))
        )


@dataclass
class RiskThresholds:
    """Limiares de classificação de risco"""
    
    low_max: float = 0.3
    medium_max: float = 0.7
    high_min: float = 0.8
    
    def classify_risk(self, score: float) -> str:
        """Classifica o nível de risco baseado no score"""
        if score <= self.low_max:
            return "Low"
        elif score <= self.medium_max:
            return "Medium"
        else:
            return "High"
