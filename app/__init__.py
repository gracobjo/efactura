from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'eFactura.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    os.makedirs(app.instance_path, exist_ok=True)
    db.init_app(app)
    
    # Configurar CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Crear nueva instancia de API para cada app
    api = Api(app)
    
    # Importar y registrar recursos aquí
    from app.routes.factura_routes import FacturaResource, VerificarFacturaResource, FacturasBusquedaResource, FacturaPDFResource, FacturaDeleteResource, MigrarFacturasResource
    api.add_resource(FacturaResource, '/factura')
    api.add_resource(VerificarFacturaResource, '/verificar/<string:id_factura>')
    api.add_resource(FacturasBusquedaResource, '/facturas')
    api.add_resource(FacturaPDFResource, '/factura/<int:id_factura>/pdf')
    api.add_resource(FacturaDeleteResource, '/factura/<int:id_factura>')
    api.add_resource(MigrarFacturasResource, '/migrar-facturas')

    with app.app_context():
        db.create_all()
    print("Rutas registradas:", [str(r) for r in app.url_map.iter_rules()])
    return app 