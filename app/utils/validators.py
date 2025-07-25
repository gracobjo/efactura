"""
Utilidades para validación de datos
"""
from app.config import Config
from app.utils.formatters import validar_identificacion, sanitizar_texto
from app.exceptions import ValidationError

def validar_cliente(cliente_data):
    """Valida los datos del cliente"""
    if not cliente_data:
        raise ValidationError("Datos del cliente requeridos")
    
    nombre = cliente_data.get('nombre')
    direccion = cliente_data.get('direccion')
    identificacion = cliente_data.get('identificacion')
    
    if not nombre or not nombre.strip():
        raise ValidationError("Nombre del cliente requerido")
    
    if not direccion or not direccion.strip():
        raise ValidationError("Dirección del cliente requerida")
    
    if not identificacion or not identificacion.strip():
        raise ValidationError("Identificación del cliente requerida")
    
    if not validar_identificacion(identificacion):
        raise ValidationError("Formato de identificación inválido")
    
    return {
        'nombre': sanitizar_texto(nombre),
        'direccion': sanitizar_texto(direccion),
        'identificacion': sanitizar_texto(identificacion)
    }

def validar_items(items_data):
    """Valida los datos de los items"""
    if not items_data or not isinstance(items_data, list):
        raise ValidationError("Lista de items requerida")
    
    if len(items_data) == 0:
        raise ValidationError("Al menos un item es requerido")
    
    items_validados = []
    for i, item in enumerate(items_data):
        if not isinstance(item, dict):
            raise ValidationError(f"Item {i+1}: formato inválido")
        
        descripcion = item.get('descripcion')
        cantidad = item.get('cantidad')
        precio = item.get('precio')
        
        if not descripcion or not descripcion.strip():
            raise ValidationError(f"Item {i+1}: descripción requerida")
        
        if cantidad is None or not isinstance(cantidad, (int, float)) or cantidad <= 0:
            raise ValidationError(f"Item {i+1}: cantidad debe ser un número positivo")
        
        if precio is None or not isinstance(precio, (int, float)) or precio < 0:
            raise ValidationError(f"Item {i+1}: precio debe ser un número no negativo")
        
        items_validados.append({
            'descripcion': sanitizar_texto(descripcion),
            'cantidad': int(cantidad) if isinstance(cantidad, float) and cantidad.is_integer() else cantidad,
            'precio': float(precio)
        })
    
    return items_validados

def validar_archivo_pdf(archivo):
    """Valida que el archivo sea un PDF válido"""
    if not archivo:
        raise ValidationError("Archivo requerido")
    
    if archivo.filename == '':
        raise ValidationError("Nombre de archivo requerido")
    
    if not archivo.filename.lower().endswith('.pdf'):
        raise ValidationError("Solo se permiten archivos PDF")
    
    # Verificar tamaño del archivo
    archivo.seek(0, 2)  # Ir al final del archivo
    tamaño = archivo.tell()
    archivo.seek(0)  # Volver al inicio
    
    if tamaño > Config.MAX_CONTENT_LENGTH:
        raise ValidationError(f"El archivo es demasiado grande. Máximo: {Config.MAX_CONTENT_LENGTH // (1024*1024)}MB")
    
    return True 