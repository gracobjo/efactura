"""
Rutas para la gestión de facturas
"""
from flask import request, send_file, jsonify
from flask_restful import Resource
from werkzeug.utils import secure_filename
import os
import tempfile

from app.models.factura import Cliente, Item, Factura
from app.services import storage, pdf_generator
from app.services.pdf_extractor import PDFExtractor
from app.utils.validators import validar_cliente, validar_items, validar_archivo_pdf
from app.utils.formatters import formatear_euros, formatear_fecha
from app.config import Config
from app.exceptions import ValidationError, FacturaNotFoundError, PDFProcessingError, StorageError

class FacturaResource(Resource):
    """Endpoint para crear nuevas facturas"""
    
    def post(self):
        """Crea una nueva factura"""
        try:
            data = request.get_json()
            if not data:
                return {'message': 'Datos JSON requeridos'}, 400
            
            # Validar datos de entrada
            cliente_data = validar_cliente(data.get('cliente'))
            items_data = validar_items(data.get('items', []))
            
            # Crear objetos del dominio
            cliente = Cliente(
                nombre=cliente_data['nombre'],
                direccion=cliente_data['direccion'],
                identificacion=cliente_data['identificacion']
            )
            
            items = [
                Item(
                    descripcion=item['descripcion'],
                    cantidad=item['cantidad'],
                    precio_unitario=item['precio']
                ) for item in items_data
            ]
            
            # Crear y guardar factura
            factura = Factura(cliente, items)
            id_factura = storage.guardar_factura(factura)
            
            # Generar PDF
            pdf_path = pdf_generator.generar_pdf(factura, id_factura)
            
            return send_file(pdf_path, as_attachment=True, download_name=f"factura_{id_factura}.pdf")
            
        except ValidationError as e:
            return {'message': str(e)}, 400
        except StorageError as e:
            return {'message': f'Error de almacenamiento: {str(e)}'}, 500
        except Exception as e:
            return {'message': f'Error interno: {str(e)}'}, 500

class VerificarFacturaResource(Resource):
    """Endpoint para verificar facturas existentes"""
    
    def get(self, id_factura):
        """Verifica una factura por ID"""
        try:
            factura = storage.obtener_factura(id_factura)
            
            total = factura.calcular_total()
            iva = total * Config.IVA_PORCENTAJE
            total_con_iva = total + iva
            
            return jsonify({
                'numero': factura.numero,
                'fecha': formatear_fecha(factura.fecha),
                'cliente': {
                    'nombre': factura.cliente.nombre,
                    'identificacion': factura.cliente.identificacion
                },
                'total': formatear_euros(total),
                'iva': formatear_euros(iva),
                'total_con_iva': formatear_euros(total_con_iva)
            })
            
        except FacturaNotFoundError as e:
            return {'message': str(e)}, 404
        except StorageError as e:
            return {'message': f'Error de almacenamiento: {str(e)}'}, 500
        except Exception as e:
            return {'message': f'Error interno: {str(e)}'}, 500

class FacturasBusquedaResource(Resource):
    """Endpoint para búsqueda avanzada de facturas"""
    
    def get(self):
        """Busca facturas con filtros opcionales"""
        try:
            from app import db
            from app.services.storage import FacturaDB, ClienteDB
            from sqlalchemy.orm import joinedload
            from sqlalchemy import and_, or_
            from datetime import datetime
            
            query = db.session.query(FacturaDB).options(joinedload(FacturaDB.cliente))
            
            # Aplicar filtros
            query = self._aplicar_filtros(query)
            
            facturas = query.all()
            result = []
            
            for f in facturas:
                total = sum(item.cantidad * (item.precio_unitario or 0) for item in f.items)
                result.append({
                    'id': f.id,
                    'numero': f.numero,
                    'fecha': formatear_fecha(f.fecha),
                    'cliente': {
                        'nombre': f.cliente.nombre if f.cliente else 'Desconocido',
                        'identificacion': f.cliente.identificacion if f.cliente else ''
                    },
                    'total': formatear_euros(total)
                })
            
            return jsonify(result)
            
        except Exception as e:
            return {'message': f'Error interno: {str(e)}'}, 500
    
    def _aplicar_filtros(self, query):
        """Aplica filtros a la consulta de facturas"""
        from app.services.storage import ClienteDB, FacturaDB
        from datetime import datetime
        
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
                fecha_desde_dt = datetime.strptime(fecha_desde, Config.DATE_FORMAT)
                query = query.filter(FacturaDB.fecha >= fecha_desde_dt)
            except ValueError:
                pass
        if fecha_hasta:
            try:
                fecha_hasta_dt = datetime.strptime(fecha_hasta, Config.DATE_FORMAT)
                query = query.filter(FacturaDB.fecha <= fecha_hasta_dt)
            except ValueError:
                pass

        return query

class FacturaPDFResource(Resource):
    """Endpoint para descargar PDF de facturas"""
    
    def get(self, id_factura):
        """Descarga el PDF de una factura"""
        try:
            factura = storage.obtener_factura(id_factura)
            pdf_path = pdf_generator.generar_pdf(factura, id_factura)
            return send_file(pdf_path, as_attachment=True, download_name=f"factura_{id_factura}.pdf")
            
        except FacturaNotFoundError as e:
            return {'message': str(e)}, 404
        except StorageError as e:
            return {'message': f'Error de almacenamiento: {str(e)}'}, 500
        except Exception as e:
            return {'message': f'Error interno: {str(e)}'}, 500

class FacturaDeleteResource(Resource):
    """Endpoint para eliminar facturas"""
    
    def delete(self, id_factura):
        """Elimina una factura"""
        try:
            storage.eliminar_factura(id_factura)
            return {'message': 'Factura eliminada correctamente'}, 200
            
        except FacturaNotFoundError as e:
            return {'message': str(e)}, 404
        except StorageError as e:
            return {'message': f'Error de almacenamiento: {str(e)}'}, 500
        except Exception as e:
            return {'message': f'Error interno: {str(e)}'}, 500

class MigrarFacturasResource(Resource):
    """Endpoint para migrar facturas PDF existentes"""
    
    def __init__(self):
        self.extractor = PDFExtractor()
    
    def post(self):
        """Migra facturas PDF a la base de datos"""
        try:
            if 'files' not in request.files:
                return {'message': 'No se han enviado archivos'}, 400
            
            files = request.files.getlist('files')
            if not files or files[0].filename == '':
                return {'message': 'No se han seleccionado archivos'}, 400
            
            facturas_migradas = []
            
            for file in files:
                try:
                    # Validar archivo
                    validar_archivo_pdf(file)
                    
                    # Guardar archivo temporal
                    filename = secure_filename(file.filename)
                    temp_path = os.path.join(tempfile.gettempdir(), filename)
                    file.save(temp_path)
                    
                    # Extraer datos del PDF
                    datos_pdf = self.extractor.extraer_datos(temp_path)
                    
                    if datos_pdf:
                        # Crear factura desde datos extraídos
                        factura = self._crear_factura_desde_datos(datos_pdf)
                        
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
                    os.remove(temp_path)
                    
                except (ValidationError, PDFProcessingError) as e:
                    print(f"Error procesando archivo {file.filename}: {e}")
                    continue
                except StorageError as e:
                    print(f"Error de almacenamiento procesando archivo {file.filename}: {e}")
                    continue
                except Exception as e:
                    print(f"Error inesperado procesando archivo {file.filename}: {e}")
                    continue
            
            return jsonify({
                'message': f'Se migraron {len(facturas_migradas)} facturas exitosamente',
                'facturas_migradas': facturas_migradas
            })
            
        except Exception as e:
            return {'message': f'Error interno: {str(e)}'}, 500
    
    def _crear_factura_desde_datos(self, datos_pdf):
        """Crea una factura a partir de datos extraídos del PDF"""
        cliente = Cliente(
            nombre=datos_pdf['cliente']['nombre'] or 'Cliente Migrado',
            direccion=datos_pdf['cliente']['direccion'] or 'Dirección no disponible',
            identificacion=datos_pdf['cliente']['identificacion'] or 'N/A'
        )
        
        items = [
            Item(
                descripcion=item['descripcion'],
                cantidad=item['cantidad'],
                precio_unitario=item['precio']
            ) for item in datos_pdf['items']
        ]
        
        return Factura(cliente, items) 