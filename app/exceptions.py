"""
Excepciones personalizadas para la aplicación
"""

class EFacturaException(Exception):
    """Excepción base para la aplicación eFactura"""
    pass

class ValidationError(EFacturaException):
    """Excepción para errores de validación de datos"""
    pass

class PDFProcessingError(EFacturaException):
    """Excepción para errores en el procesamiento de PDFs"""
    pass

class StorageError(EFacturaException):
    """Excepción para errores de almacenamiento"""
    pass

class FacturaNotFoundError(EFacturaException):
    """Excepción para facturas no encontradas"""
    pass

class ConfigurationError(EFacturaException):
    """Excepción para errores de configuración"""
    pass 