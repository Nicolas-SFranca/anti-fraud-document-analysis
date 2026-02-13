"""
Analisador de Fraude
Utiliza Azure OpenAI para análise de risco de fraude em documentos
"""

import json
import logging
from typing import Dict
from openai import AzureOpenAI

from app.config import AzureConfig, RiskThresholds


logger = logging.getLogger(__name__)


class FraudAnalyzer:
    """Analisador de risco de fraude usando LLM"""
    
    def __init__(self, config: AzureConfig):
        """
        Inicializa o analisador de fraude
        
        Args:
            config: Configurações do Azure
        """
        self.config = config
        self.thresholds = RiskThresholds()
        
        self.client = AzureOpenAI(
            api_key=config.openai_key,
            api_version=config.openai_api_version,
            azure_endpoint=config.openai_endpoint
        )
    
    def analyze_fraud_risk(self, document_text: str, metadata: Dict = None) -> Dict:
        """
        Analisa o risco de fraude em um documento
        
        Args:
            document_text: Texto extraído do documento
            metadata: Metadados opcionais do documento
            
        Returns:
            Dicionário com análise de risco estruturada
        """
        try:
            logger.info("Iniciando análise de fraude")
            
            system_prompt = self._build_system_prompt()
            user_prompt = self._build_user_prompt(document_text, metadata)
            
            response = self.client.chat.completions.create(
                model=self.config.openai_deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=1000,
                response_format={"type": "json_object"}
            )
            
            analysis_result = json.loads(response.choices[0].message.content)
            
            # Adiciona classificação de risco
            risk_score = analysis_result.get("risk_score", 0.0)
            analysis_result["risk_level"] = self.thresholds.classify_risk(risk_score)
            
            logger.info(f"Análise concluída: Score {risk_score}, Nível {analysis_result['risk_level']}")
            
            return {
                "success": True,
                "analysis": analysis_result
            }
            
        except Exception as e:
            logger.error(f"Erro na análise de fraude: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "analysis": None
            }
    
    def _build_system_prompt(self) -> str:
        """Constrói o prompt de sistema para o modelo"""
        return """Você é um especialista em detecção de fraudes em documentos.

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

Não inclua nenhum texto fora do JSON."""
    
    def _build_user_prompt(self, document_text: str, metadata: Dict = None) -> str:
        """
        Constrói o prompt do usuário para análise
        
        Args:
            document_text: Texto do documento
            metadata: Metadados opcionais
            
        Returns:
            Prompt formatado
        """
        prompt = f"Analise o seguinte documento em busca de sinais de fraude:\n\n{document_text}"
        
        if metadata:
            prompt += f"\n\nMetadados do documento:\n{json.dumps(metadata, indent=2, ensure_ascii=False)}"
        
        return prompt
    
    def validate_analysis_format(self, analysis: Dict) -> bool:
        """
        Valida se a análise está no formato esperado
        
        Args:
            analysis: Dicionário com resultado da análise
            
        Returns:
            True se válido, False caso contrário
        """
        required_fields = ["risk_score", "justification", "suspicious_elements", "recommendations"]
        
        if not all(field in analysis for field in required_fields):
            return False
        
        if not (0.0 <= analysis["risk_score"] <= 1.0):
            return False
        
        if not isinstance(analysis["suspicious_elements"], list):
            return False
        
        if not isinstance(analysis["recommendations"], list):
            return False
        
        return True
