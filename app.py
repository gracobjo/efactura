#!/usr/bin/env python3
"""
Aplicación principal de eFactura
Sistema de Facturación Electrónica
"""

from app import create_app
from flask_cors import CORS
from flask import request, jsonify

# Crear la aplicación Flask
app = create_app()

# Configurar CORS adicional para desarrollo
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

@app.route('/')
def index():
    """Página principal"""
    return jsonify({
        "message": "eFactura API - Sistema de Facturación Electrónica",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "facturas": "/api/facturas",
            "procesar": "/api/procesar-factura",
            "validar": "/api/validar-factura",
            "calcular": "/api/calcular-total"
        }
    })

@app.route('/health')
def health():
    """Endpoint de salud de la API"""
    return jsonify({
        "status": "healthy",
        "service": "eFactura API",
        "timestamp": "2024-01-01T00:00:00Z"
    })

@app.route('/api/facturas', methods=['GET', 'POST'])
def api_facturas():
    """Endpoint principal de facturas para el simulador"""
    if request.method == 'GET':
        # Devolver lista de facturas
        try:
            from app.services import storage
            facturas = storage.listar_facturas()
            return jsonify({
                "message": "Facturas obtenidas exitosamente",
                "count": len(facturas),
                "facturas": [
                    {
                        "id": factura.numero,
                        "cliente": factura.cliente.nombre,
                        "fecha": factura.fecha.strftime("%Y-%m-%d"),
                        "total": factura.calcular_total()
                    } for factura in facturas
                ]
            })
        except Exception as e:
            return jsonify({"message": f"Error al obtener facturas: {str(e)}"}), 500
    
    elif request.method == 'POST':
        # Crear nueva factura
        try:
            data = request.get_json()
            if not data:
                return jsonify({'message': 'Datos JSON requeridos'}), 400
            
            from app.utils.validators import validar_cliente, validar_items
            from app.models.factura import Cliente, Item, Factura
            from app.services import storage, pdf_generator
            
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
            
            return jsonify({
                "message": "Factura creada exitosamente",
                "id": id_factura,
                "numero": factura.numero,
                "cliente": factura.cliente.nombre,
                "total": factura.calcular_total()
            }), 201
            
        except Exception as e:
            return jsonify({'message': f'Error al crear factura: {str(e)}'}), 500

@app.route('/api/procesar-factura', methods=['POST'])
def procesar_factura():
    """Procesa una factura externa sin guardarla en BD"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Datos JSON requeridos'}), 400
        
        from app.utils.validators import validar_cliente, validar_items
        from app.models.factura import Cliente, Item, Factura
        
        # Validar datos de entrada
        cliente_data = validar_cliente(data.get('cliente'))
        items_data = validar_items(data.get('items', []))
        
        # Crear objetos del dominio (sin guardar en BD)
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
        
        # Crear factura temporal
        factura = Factura(cliente, items)
        
        # Procesar y devolver resultados
        return jsonify({
            "message": "Factura procesada exitosamente",
            "numero": factura.numero,
            "cliente": {
                "nombre": factura.cliente.nombre,
                "direccion": factura.cliente.direccion,
                "identificacion": factura.cliente.identificacion
            },
            "items": [
                {
                    "descripcion": item.descripcion,
                    "cantidad": item.cantidad,
                    "precio_unitario": item.precio_unitario,
                    "subtotal": item.subtotal()
                } for item in factura.items
            ],
            "total": factura.calcular_total(),
            "fecha": factura.fecha.strftime("%Y-%m-%d"),
            "procesado_en": "eFactura API"
        })
        
    except Exception as e:
        return jsonify({'message': f'Error al procesar factura: {str(e)}'}), 500

@app.route('/api/validar-factura', methods=['POST'])
def validar_factura():
    """Valida una factura sin procesarla"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Datos JSON requeridos'}), 400
        
        from app.utils.validators import validar_cliente, validar_items
        
        # Validar datos
        cliente_data = validar_cliente(data.get('cliente'))
        items_data = validar_items(data.get('items', []))
        
        return jsonify({
            "message": "Factura válida",
            "cliente_valido": True,
            "items_validos": len(items_data),
            "total_items": len(data.get('items', [])),
            "errores": []
        })
        
    except Exception as e:
        return jsonify({
            "message": "Factura inválida",
            "cliente_valido": False,
            "items_validos": 0,
            "total_items": len(data.get('items', [])) if data else 0,
            "errores": [str(e)]
        }), 400

@app.route('/api/calcular-total', methods=['POST'])
def calcular_total():
    """Calcula el total de una factura sin procesarla completamente"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Datos JSON requeridos'}), 400
        
        items = data.get('items', [])
        total = 0.0
        subtotales = []
        
        for item in items:
            cantidad = item.get('cantidad', 0) or 0
            precio = item.get('precio', 0.0) or 0.0
            subtotal = cantidad * precio
            subtotales.append({
                "descripcion": item.get('descripcion', ''),
                "cantidad": cantidad,
                "precio": precio,
                "subtotal": subtotal
            })
            total += subtotal
        
        return jsonify({
            "message": "Total calculado exitosamente",
            "subtotales": subtotales,
            "total": total,
            "cantidad_items": len(items)
        })
        
    except Exception as e:
        return jsonify({'message': f'Error al calcular total: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 Iniciando eFactura API...")
    print("📍 URL: http://localhost:5000")
    print("🔗 API: http://localhost:5000/api/facturas")
    print("🔄 Procesar: http://localhost:5000/api/procesar-factura")
    print("✅ Validar: http://localhost:5000/api/validar-factura")
    print("🧮 Calcular: http://localhost:5000/api/calcular-total")
    print("🏥 Health: http://localhost:5000/health")
    print("🛑 Para detener: Ctrl+C")
    print("-" * 50)
    
    # Ejecutar la aplicación en modo desarrollo
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    ) 