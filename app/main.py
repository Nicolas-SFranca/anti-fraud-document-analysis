"""
Sistema de Análise Anti-Fraude de Documentos
Orquestra a extração de documentos e análise de risco
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv

from app.config import AzureConfig
from app.document_service import DocumentService
from app.fraud_analyzer import FraudAnalyzer


# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('anti_fraud_analysis.log')
    ]
)

logger = logging.getLogger(__name__)


class AntiFraudSystem:
    """Sistema principal de análise anti-fraude"""
    
    def __init__(self):
        """Inicializa o sistema carregando configurações"""
        load_dotenv()
        
        try:
            self.config = AzureConfig.from_environment()
            self.document_service = DocumentService(self.config)
            self.fraud_analyzer = FraudAnalyzer(self.config)
            logger.info("Sistema inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar sistema: {str(e)}")
            raise
    
    def process_document(self, file_path: str) -> Dict:
        """
        Processa um documento completo: extração e análise
        
        Args:
            file_path: Caminho do arquivo a ser processado
            
        Returns:
            Resultado completo da análise
        """
        logger.info(f"Iniciando processamento de: {file_path}")
        
        # Etapa 1: Extração de texto
        extraction_result = self.document_service.extract_text_from_file(file_path)
        
        if not extraction_result["success"]:
            return {
                "success": False,
                "stage": "extraction",
                "error": extraction_result.get("error", "Erro desconhecido"),
                "file": file_path
            }
        
        document_text = extraction_result["text"]
        metadata = extraction_result["metadata"]
        
        logger.info(f"Texto extraído: {len(document_text)} caracteres")
        
        # Etapa 2: Análise de fraude
        analysis_result = self.fraud_analyzer.analyze_fraud_risk(document_text, metadata)
        
        if not analysis_result["success"]:
            return {
                "success": False,
                "stage": "analysis",
                "error": analysis_result.get("error", "Erro desconhecido"),
                "file": file_path,
                "extraction": extraction_result
            }
        
        # Resultado final
        final_result = {
            "success": True,
            "file": file_path,
            "extraction": {
                "text_length": len(document_text),
                "metadata": metadata
            },
            "fraud_analysis": analysis_result["analysis"]
        }
        
        logger.info(
            f"Processamento concluído - Risco: {final_result['fraud_analysis']['risk_level']}, "
            f"Score: {final_result['fraud_analysis']['risk_score']}"
        )
        
        return final_result
    
    def process_document_url(self, document_url: str) -> Dict:
        """
        Processa um documento a partir de URL
        
        Args:
            document_url: URL do documento
            
        Returns:
            Resultado completo da análise
        """
        logger.info(f"Iniciando processamento de URL: {document_url}")
        
        extraction_result = self.document_service.extract_text_from_url(document_url)
        
        if not extraction_result["success"]:
            return {
                "success": False,
                "stage": "extraction",
                "error": extraction_result.get("error", "Erro desconhecido"),
                "url": document_url
            }
        
        document_text = extraction_result["text"]
        metadata = extraction_result["metadata"]
        
        analysis_result = self.fraud_analyzer.analyze_fraud_risk(document_text, metadata)
        
        if not analysis_result["success"]:
            return {
                "success": False,
                "stage": "analysis",
                "error": analysis_result.get("error", "Erro desconhecido"),
                "url": document_url,
                "extraction": extraction_result
            }
        
        final_result = {
            "success": True,
            "url": document_url,
            "extraction": {
                "text_length": len(document_text),
                "metadata": metadata
            },
            "fraud_analysis": analysis_result["analysis"]
        }
        
        logger.info(
            f"Processamento de URL concluído - Risco: {final_result['fraud_analysis']['risk_level']}"
        )
        
        return final_result
    
    def save_result(self, result: Dict, output_path: str = None):
        """
        Salva resultado da análise em arquivo JSON
        
        Args:
            result: Resultado da análise
            output_path: Caminho do arquivo de saída (opcional)
        """
        if output_path is None:
            output_path = "fraud_analysis_result.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Resultado salvo em: {output_path}")


def main():
    """Função principal de exemplo"""
    
    # Verifica se foi passado um arquivo como argumento
    if len(sys.argv) < 2:
        print("Uso: python main.py <caminho_do_documento>")
        print("Exemplo: python main.py examples/sample_document.pdf")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"Erro: Arquivo não encontrado - {file_path}")
        sys.exit(1)
    
    # Inicializa e executa
    system = AntiFraudSystem()
    result = system.process_document(file_path)
    
    # Exibe resultado
    print("\n" + "="*80)
    print("RESULTADO DA ANÁLISE ANTI-FRAUDE")
    print("="*80)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Salva resultado
    output_file = f"result_{Path(file_path).stem}.json"
    system.save_result(result, output_file)
    
    print(f"\nResultado salvo em: {output_file}")


if __name__ == "__main__":
    main()
