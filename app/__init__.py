from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app(config_name='default'):
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Cargar configuración
    from app.config import config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Configurar CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Crear API
    api = Api(app)
    
    # Registrar rutas
    from app.routes.factura_routes import (
        FacturaResource, 
        VerificarFacturaResource, 
        FacturasBusquedaResource, 
        FacturaPDFResource, 
        FacturaDeleteResource, 
        MigrarFacturasResource
    )
    
    api.add_resource(FacturaResource, '/factura')
    api.add_resource(VerificarFacturaResource, '/verificar/<string:id_factura>')
    api.add_resource(FacturasBusquedaResource, '/facturas')
    api.add_resource(FacturaPDFResource, '/factura/<int:id_factura>/pdf')
    api.add_resource(FacturaDeleteResource, '/factura/<int:id_factura>')
    api.add_resource(MigrarFacturasResource, '/migrar-facturas')

    # Crear tablas de base de datos
    with app.app_context():
        db.create_all()
    
    return app 