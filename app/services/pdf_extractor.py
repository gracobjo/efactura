"""
Servicio para extracción de datos de facturas PDF
"""
import os
import re
import PyPDF2
from typing import Dict, Optional, List
from app.config import Config
from app.exceptions import PDFProcessingError

class PDFExtractor:
    """Clase para extraer datos de facturas PDF"""
    
    def __init__(self):
        self.patterns = {
            'numero_factura': [
                r'[Ff]actura\s*[Nn]°?\s*:?\s*([A-Z0-9\-]+)',
                r'[Nn]úmero\s*[Dd]e\s*[Ff]actura\s*:?\s*([A-Z0-9\-]+)',
                r'[Ff]actura\s*([A-Z0-9\-]+)'
            ],
            'fecha': [
                r'[Ff]echa\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'[Ff]echa\s*:?\s*(\d{2}/\d{2}/\d{4})'
            ],
            'total': [
                r'[Tt]otal\s*:?\s*([0-9,]+\.?[0-9]*)\s*[€EUR]',
                r'[Tt]otal\s*[Gg]eneral\s*:?\s*([0-9,]+\.?[0-9]*)',
                r'[Aa] [Pp]agar\s*:?\s*([0-9,]+\.?[0-9]*)'
            ],
            'cliente_nombre': [
                r'[Cc]liente\s*:?\s*([^\n]+)',
                r'[Dd]estinatario\s*:?\s*([^\n]+)',
                r'[Ss]eñor(?:es)?\s*:?\s*([^\n]+)'
            ],
            'cliente_identificacion': [
                r'[Nn]IF\s*:?\s*([A-Z0-9]+)',
                r'[Cc]IF\s*:?\s*([A-Z0-9]+)',
                r'[Dd]NI\s*:?\s*([A-Z0-9]+)'
            ]
        }
    
    def extraer_datos(self, pdf_path: str) -> Optional[Dict]:
        """
        Extrae datos de una factura PDF
        
        Args:
            pdf_path: Ruta al archivo PDF
            
        Returns:
            Diccionario con los datos extraídos o None si hay error
        """
        try:
            if not os.path.exists(pdf_path):
                raise PDFProcessingError(f"Archivo no encontrado: {pdf_path}")
            
            texto = self._extraer_texto_pdf(pdf_path)
            if not texto:
                raise PDFProcessingError("No se pudo extraer texto del PDF")
            
            datos = self._procesar_texto(texto)
            return datos
            
        except PDFProcessingError:
            raise
        except Exception as e:
            raise PDFProcessingError(f"Error extrayendo datos del PDF {pdf_path}: {e}")
    
    def _extraer_texto_pdf(self, pdf_path: str) -> str:
        """Extrae todo el texto del PDF"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                texto = ""
                for page in pdf_reader.pages:
                    texto += page.extract_text()
                return texto
        except Exception as e:
            raise PDFProcessingError(f"Error leyendo PDF: {e}")
    
    def _procesar_texto(self, texto: str) -> Dict:
        """Procesa el texto extraído y extrae los datos relevantes"""
        datos = {
            'cliente': {
                'nombre': '',
                'direccion': '',
                'identificacion': ''
            },
            'items': [],
            'numero_factura': '',
            'fecha': '',
            'total': 0
        }
        
        # Extraer número de factura
        datos['numero_factura'] = self._extraer_campo(texto, 'numero_factura')
        
        # Extraer fecha
        datos['fecha'] = self._extraer_campo(texto, 'fecha')
        
        # Extraer total
        total_str = self._extraer_campo(texto, 'total')
        if total_str:
            try:
                datos['total'] = float(total_str.replace(',', ''))
            except ValueError:
                datos['total'] = 0
        
        # Extraer datos del cliente
        datos['cliente']['nombre'] = self._extraer_campo(texto, 'cliente_nombre')
        datos['cliente']['identificacion'] = self._extraer_campo(texto, 'cliente_identificacion')
        
        # Crear item genérico basado en el total
        if datos['total'] > 0:
            datos['items'] = [{
                'descripcion': 'Servicio migrado desde factura anterior',
                'cantidad': 1,
                'precio': datos['total']
            }]
        
        return datos
    
    def _extraer_campo(self, texto: str, campo: str) -> str:
        """Extrae un campo específico usando los patrones definidos"""
        for patron in self.patterns[campo]:
            match = re.search(patron, texto)
            if match:
                return match.group(1).strip()
        return ""
    
    def extraer_multiples_pdfs(self, pdf_paths: List[str]) -> List[Dict]:
        """
        Extrae datos de múltiples PDFs
        
        Args:
            pdf_paths: Lista de rutas a archivos PDF
            
        Returns:
            Lista de diccionarios con los datos extraídos
        """
        resultados = []
        for pdf_path in pdf_paths:
            try:
                datos = self.extraer_datos(pdf_path)
                if datos:
                    datos['archivo_origen'] = os.path.basename(pdf_path)
                    resultados.append(datos)
            except PDFProcessingError as e:
                print(f"Error procesando {pdf_path}: {e}")
                continue
        return resultados 