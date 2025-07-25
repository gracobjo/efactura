import os
from datetime import datetime

class Config:
    """Configuración centralizada de la aplicación"""
    
    # Configuración de base de datos
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'instance', 'eFactura.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de archivos
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'instance', 'uploads')
    FACTURAS_FOLDER = os.path.join(os.getcwd(), 'instance', 'facturas')
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Configuración de facturación
    IVA_PORCENTAJE = 0.21  # 21% de IVA
    BASE_URL_VERIFICACION = "http://localhost:5000/verificar/"
    
    # Configuración de seguridad
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Configuración de formato
    DATE_FORMAT = '%Y-%m-%d'
    CURRENCY_FORMAT = 'EUR'
    
    @staticmethod
    def init_app(app):
        """Inicializar configuración en la aplicación Flask"""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.FACTURAS_FOLDER, exist_ok=True)

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    # En producción, cambiar la URL de verificación
    BASE_URL_VERIFICACION = "https://tu-dominio.com/verificar/"

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 