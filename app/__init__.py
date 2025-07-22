from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import os

db = SQLAlchemy()
api = Api()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'eFactura.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    os.makedirs(app.instance_path, exist_ok=True)
    db.init_app(app)
    api.init_app(app)

    # Importar y registrar recursos aquí
    from app.routes.factura_routes import FacturaResource, VerificarFacturaResource
    api.add_resource(FacturaResource, '/factura')
    api.add_resource(VerificarFacturaResource, '/verificar/<string:id_factura>')

     # <--- AGREGA ESTO ANTES DEL RETURN
    with app.app_context():
        db.create_all()

    return app 