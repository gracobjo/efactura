from flask import request, send_file, jsonify
from flask_restful import Resource
from app.models.factura import Cliente, Item, Factura
import os

# Suponiendo que storage.py y pdf_generator.py estarán implementados
from app.services import storage, pdf_generator

IVA_PORCENTAJE = 0.21  # 21% de IVA

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
            return {'mensaje': 'Factura no encontrada'}, 404
        total = factura.calcular_total()
        iva = total * IVA_PORCENTAJE
        total_con_iva = total + iva
        # Devolver datos básicos
        return jsonify({
            'numero': factura.numero,
            'fecha': factura.fecha.strftime('%Y-%m-%d'),
            'cliente': {
                'nombre': factura.cliente.nombre,
                'identificacion': factura.cliente.identificacion
            },
            'total': total,
            'iva': iva,
            'total_con_iva': total_con_iva
        })

# ENDPOINT AVANZADO: GET /facturas (búsqueda avanzada)
from app import db
from app.services.storage import FacturaDB, ClienteDB
from sqlalchemy.orm import joinedload
from sqlalchemy import and_, or_
from datetime import datetime

class FacturasBusquedaResource(Resource):
    def get(self):
        query = db.session.query(FacturaDB).options(joinedload(FacturaDB.cliente))
        # Filtros
        cliente_nombre = request.args.get('cliente_nombre')
        cliente_identificacion = request.args.get('cliente_identificacion')
        fecha_desde = request.args.get('fecha_desde')
        fecha_hasta = request.args.get('fecha_hasta')
        total_min = request.args.get('total_min', type=float)
        total_max = request.args.get('total_max', type=float)

        if cliente_nombre:
            query = query.join(FacturaDB.cliente).filter(ClienteDB.nombre.ilike(f"%{cliente_nombre}%"))
        if cliente_identificacion:
            query = query.join(FacturaDB.cliente).filter(ClienteDB.identificacion == cliente_identificacion)
        if fecha_desde:
            try:
                fecha_desde_dt = datetime.strptime(fecha_desde, "%Y-%m-%d")
                query = query.filter(FacturaDB.fecha >= fecha_desde_dt)
            except Exception:
                pass
        if fecha_hasta:
            try:
                fecha_hasta_dt = datetime.strptime(fecha_hasta, "%Y-%m-%d")
                query = query.filter(FacturaDB.fecha <= fecha_hasta_dt)
            except Exception:
                pass

        facturas = query.all()
        result = []
        for f in facturas:
            total = sum(item.cantidad * item.precio_unitario for item in f.items)
            if (total_min is not None and total < total_min) or (total_max is not None and total > total_max):
                continue
            result.append({
                'id': f.id,
                'numero': f.numero,
                'fecha': f.fecha.strftime('%Y-%m-%d'),
                'cliente': {
                    'nombre': f.cliente.nombre if f.cliente else 'Desconocido',
                    'identificacion': f.cliente.identificacion if f.cliente else ''
                },
                'total': total
            })
        return jsonify(result)

# ENDPOINT AVANZADO: GET /factura/<id_factura>/pdf (descargar PDF)
class FacturaPDFResource(Resource):
    def get(self, id_factura):
        factura = storage.obtener_factura(id_factura)
        if not factura:
            return {'message': 'Factura no encontrada'}, 404
        pdf_path = pdf_generator.generar_pdf(factura, id_factura)
        return send_file(pdf_path, as_attachment=True)

# ENDPOINT AVANZADO: DELETE /factura/<id_factura> (eliminar factura)
class FacturaDeleteResource(Resource):
    def delete(self, id_factura):
        from app.services.storage import FacturaDB
        from app import db
        factura_db = FacturaDB.query.get(id_factura)
        if not factura_db:
            return {'message': 'Factura no encontrada'}, 404
        db.session.delete(factura_db)
        db.session.commit()
        return {'message': 'Factura eliminada correctamente'}, 200 