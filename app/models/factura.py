class Cliente:
    def __init__(self, nombre, direccion, identificacion):
        self.nombre = nombre
        self.direccion = direccion
        self.identificacion = identificacion


class Item:
    def __init__(self, descripcion, cantidad, precio_unitario):
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

    def subtotal(self):
        return self.cantidad * self.precio_unitario


import uuid
from datetime import datetime

class Factura:
    def __init__(self, cliente, items, fecha=None, numero=None):
        self.cliente = cliente  # instancia de Cliente
        self.items = items      # lista de instancias Item
        self.fecha = fecha or datetime.now()
        self.numero = numero or self.generar_numero_factura()

    def calcular_total(self):
        return sum(item.subtotal() for item in self.items)

    def generar_numero_factura(self):
        # Genera un número único usando UUID y fecha
        return f"FAC-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    def exportar_a_pdf(self, ruta_pdf):
        # Este método será implementado en services/pdf_generator.py
        # Aquí solo se deja el stub para la interfaz
        raise NotImplementedError("Implementar en pdf_generator.py") 