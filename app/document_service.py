"""
Serviço de Extração de Documentos
Utiliza Azure Document Intelligence para extrair texto de documentos
"""

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from typing import Dict, Optional
import logging

from app.config import AzureConfig


logger = logging.getLogger(__name__)


class DocumentService:
    """Serviço responsável pela extração de texto de documentos"""
    
    def __init__(self, config: AzureConfig):
        """
        Inicializa o serviço de documentos
        
        Args:
            config: Configurações do Azure
        """
        self.config = config
        self.client = DocumentAnalysisClient(
            endpoint=config.document_intelligence_endpoint,
            credential=AzureKeyCredential(config.document_intelligence_key)
        )
    
    def extract_text_from_file(self, file_path: str) -> Dict[str, any]:
        """
        Extrai texto de um arquivo de documento
        
        Args:
            file_path: Caminho do arquivo a ser processado
            
        Returns:
            Dicionário contendo texto extraído e metadados
        """
        try:
            logger.info(f"Iniciando extração de texto: {file_path}")
            
            with open(file_path, "rb") as f:
                poller = self.client.begin_analyze_document(
                    "prebuilt-document",
                    document=f
                )
            
            result = poller.result()
            
            # Extrai todo o texto do documento
            full_text = result.content
            
            # Extrai informações adicionais
            metadata = {
                "page_count": len(result.pages),
                "language": result.languages[0].locale if result.languages else "unknown",
                "confidence": self._calculate_average_confidence(result)
            }
            
            logger.info(f"Extração concluída: {metadata['page_count']} páginas")
            
            return {
                "text": full_text,
                "metadata": metadata,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Erro ao extrair texto: {str(e)}")
            return {
                "text": "",
                "metadata": {},
                "success": False,
                "error": str(e)
            }
    
    def extract_text_from_url(self, document_url: str) -> Dict[str, any]:
        """
        Extrai texto de um documento a partir de URL
        
        Args:
            document_url: URL do documento
            
        Returns:
            Dicionário contendo texto extraído e metadados
        """
        try:
            logger.info(f"Iniciando extração de texto de URL: {document_url}")
            
            poller = self.client.begin_analyze_document_from_url(
                "prebuilt-document",
                document_url=document_url
            )
            
            result = poller.result()
            full_text = result.content
            
            metadata = {
                "page_count": len(result.pages),
                "language": result.languages[0].locale if result.languages else "unknown",
                "confidence": self._calculate_average_confidence(result)
            }
            
            logger.info(f"Extração de URL concluída: {metadata['page_count']} páginas")
            
            return {
                "text": full_text,
                "metadata": metadata,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Erro ao extrair texto de URL: {str(e)}")
            return {
                "text": "",
                "metadata": {},
                "success": False,
                "error": str(e)
            }
    
    def _calculate_average_confidence(self, result) -> float:
        """
        Calcula a confiança média da extração
        
        Args:
            result: Resultado da análise do documento
            
        Returns:
            Valor médio de confiança (0.0 a 1.0)
        """
        if not result.pages:
            return 0.0
        
        total_confidence = 0.0
        word_count = 0
        
        for page in result.pages:
            for line in page.lines:
                if hasattr(line, 'confidence') and line.confidence:
                    total_confidence += line.confidence
                    word_count += 1
        
        return total_confidence / word_count if word_count > 0 else 0.0
