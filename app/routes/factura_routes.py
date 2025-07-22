from flask import request, send_file, jsonify
from flask_restful import Resource
from app.models.factura import Cliente, Item, Factura
import os

# Suponiendo que storage.py y pdf_generator.py estarán implementados
from app.services import storage, pdf_generator

class FacturaResource(Resource):
    def post(self):
        data = request.get_json()
        cliente_data = data.get('cliente')
        items_data = data.get('items', [])

        if not cliente_data or not items_data:
            return {'message': 'Datos de cliente e items requeridos'}, 400

        cliente = Cliente(
            nombre=cliente_data.get('nombre'),
            direccion=cliente_data.get('direccion'),
            identificacion=cliente_data.get('identificacion')
        )
        items = [Item(
            descripcion=item.get('descripcion'),
            cantidad=item.get('cantidad'),
            precio_unitario=item.get('precio_unitario')
        ) for item in items_data]

        factura = Factura(cliente, items)
        # Guardar en base de datos y obtener id
        id_factura = storage.guardar_factura(factura)
        # Generar PDF
        pdf_path = pdf_generator.generar_pdf(factura, id_factura)
        # Devolver el PDF generado
        return send_file(pdf_path, as_attachment=True)

class VerificarFacturaResource(Resource):
    def get(self, id_factura):
        factura = storage.obtener_factura(id_factura)
        if not factura:
            return {'message': 'Factura no encontrada'}, 404
        # Devolver datos básicos
        return jsonify({
            'numero': factura.numero,
            'fecha': factura.fecha.strftime('%Y-%m-%d'),
            'cliente': {
                'nombre': factura.cliente.nombre,
                'identificacion': factura.cliente.identificacion
            },
            'total': factura.calcular_total()
        }) 