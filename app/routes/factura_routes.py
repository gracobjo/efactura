from flask import request, send_file, jsonify
from flask_restful import Resource
from app.models.factura import Cliente, Item, Factura
import os
import PyPDF2
import re
from werkzeug.utils import secure_filename
import tempfile

# Suponiendo que storage.py y pdf_generator.py estarán implementados
from app.services import storage, pdf_generator

IVA_PORCENTAJE = 0.21  # 21% de IVA

def formatear_euros(valor):
    """Formatea un valor numérico en formato español con símbolo de euro"""
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " EUR"

# Configuración para carga de archivos
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'instance', 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extraer_datos_factura_pdf(pdf_path):
    """Extrae datos de una factura PDF existente"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        
        # Patrones para extraer información (ajustar según el formato de las facturas)
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
        numero_match = re.search(r'[Ff]actura\s*[Nn]°?\s*:?\s*([A-Z0-9\-]+)', text)
        if numero_match:
            datos['numero_factura'] = numero_match.group(1)
        
        # Extraer fecha
        fecha_match = re.search(r'[Ff]echa\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text)
        if fecha_match:
            datos['fecha'] = fecha_match.group(1)
        
        # Extraer total
        total_match = re.search(r'[Tt]otal\s*:?\s*([0-9,]+\.?[0-9]*)', text)
        if total_match:
            total_str = total_match.group(1).replace(',', '')
            datos['total'] = float(total_str)
        
        # Extraer nombre del cliente (patrón básico)
        cliente_match = re.search(r'[Cc]liente\s*:?\s*([^\n]+)', text)
        if cliente_match:
            datos['cliente']['nombre'] = cliente_match.group(1).strip()
        
        # Crear un ítem genérico basado en el total
        if datos['total'] > 0:
            datos['items'] = [{
                'descripcion': 'Servicio migrado desde factura anterior',
                'cantidad': 1,
                'precio': datos['total']
            }]
        
        return datos
        
    except Exception as e:
        print(f"Error extrayendo datos del PDF: {e}")
        return None

class MigrarFacturasResource(Resource):
    def post(self):
        """Endpoint para cargar y migrar facturas PDF existentes"""
        if 'files' not in request.files:
            return {'message': 'No se han enviado archivos'}, 400
        
        files = request.files.getlist('files')
        if not files or files[0].filename == '':
            return {'message': 'No se han seleccionado archivos'}, 400
        
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        facturas_migradas = []
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                
                # Extraer datos del PDF
                datos_pdf = extraer_datos_factura_pdf(file_path)
                
                if datos_pdf:
                    # Crear cliente
                    cliente = Cliente(
                        nombre=datos_pdf['cliente']['nombre'] or 'Cliente Migrado',
                        direccion=datos_pdf['cliente']['direccion'] or 'Dirección no disponible',
                        identificacion=datos_pdf['cliente']['identificacion'] or 'N/A'
                    )
                    
                    # Crear items
                    items = []
                    for item_data in datos_pdf['items']:
                        items.append(Item(
                            descripcion=item_data['descripcion'],
                            cantidad=item_data['cantidad'],
                            precio_unitario=item_data['precio']
                        ))
                    
                    # Crear factura
                    factura = Factura(cliente, items)
                    
                    # Guardar en base de datos
                    id_factura = storage.guardar_factura(factura)
                    
                    # Generar nuevo PDF con QR
                    pdf_path = pdf_generator.generar_pdf(factura, id_factura)
                    
                    facturas_migradas.append({
                        'archivo_original': filename,
                        'id_factura_nueva': id_factura,
                        'numero_factura': factura.numero,
                        'total': formatear_euros(factura.calcular_total()),
                        'pdf_nuevo': f"/factura/{id_factura}/pdf"
                    })
                
                # Limpiar archivo temporal
                os.remove(file_path)
        
        return jsonify({
            'message': f'Se migraron {len(facturas_migradas)} facturas exitosamente',
            'facturas_migradas': facturas_migradas
        })

class FacturaResource(Resource):
    def post(self):
        data = request.get_json()
        print("Datos recibidos:", data)  # Debug log
        cliente_data = data.get('cliente')
        items_data = data.get('items', [])

        if not cliente_data or not items_data:
            return {'message': 'Datos de cliente e items requeridos'}, 400

        cliente = Cliente(
            nombre=cliente_data.get('nombre'),
            direccion=cliente_data.get('direccion'),
            identificacion=cliente_data.get('identificacion')
        )
        items = []
        for item in items_data:
            descripcion = item.get('descripcion')
            cantidad = item.get('cantidad')
            precio = item.get('precio')
            
            print(f"Procesando item: descripcion={descripcion}, cantidad={cantidad}, precio={precio}")  # Debug log
            
            if not descripcion or cantidad is None or precio is None:
                return {'message': 'Todos los campos de items son requeridos (descripcion, cantidad, precio)'}, 400
            
            items.append(Item(
                descripcion=descripcion,
                cantidad=cantidad,
                precio_unitario=precio
            ))

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
            'total': formatear_euros(total),
            'iva': formatear_euros(iva),
            'total_con_iva': formatear_euros(total_con_iva)
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
            total = sum(item.cantidad * (item.precio_unitario or 0) for item in f.items)
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
                'total': formatear_euros(total)
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
        factura_db = db.session.get(FacturaDB, id_factura)
        if not factura_db:
            return {'message': 'Factura no encontrada'}, 404
        db.session.delete(factura_db)
        db.session.commit()
        return {'message': 'Factura eliminada correctamente'}, 200 