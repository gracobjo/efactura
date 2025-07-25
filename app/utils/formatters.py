"""
Utilidades para formateo de datos
"""
from app.config import Config

def formatear_euros(valor):
    """Formatea un valor numérico en formato español con símbolo de euro"""
    if valor is None:
        return "0,00 EUR"
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " " + Config.CURRENCY_FORMAT

def formatear_fecha(fecha):
    """Formatea una fecha según la configuración"""
    if fecha is None:
        return ""
    return fecha.strftime(Config.DATE_FORMAT)

def validar_identificacion(identificacion):
    """Valida formato básico de identificación fiscal"""
    if not identificacion:
        return False
    # Validación básica: debe tener al menos 8 caracteres
    return len(identificacion.strip()) >= 8

def sanitizar_texto(texto, max_length=255):
    """Sanitiza texto para evitar inyección y limita longitud"""
    if not texto:
        return ""
    # Eliminar caracteres peligrosos y limitar longitud
    sanitized = str(texto).strip()[:max_length]
    return sanitized.replace('<', '&lt;').replace('>', '&gt;') 