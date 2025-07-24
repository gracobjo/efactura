import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app, db

@pytest.fixture
def app():
    # Limpiar cualquier estado previo
    if 'app' in globals():
        del globals()['app']
    
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })
    # Establecer variable de entorno para testing
    os.environ['TESTING'] = 'True'
    with app.app_context():
        db.create_all()
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def limpiar_bd(app):
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all() 