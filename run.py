#!/usr/bin/env python3
"""
Archivo principal para ejecutar la aplicación eFactura
"""
import os
from app import create_app

# Configurar el entorno
config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=config_name == 'development'
    ) 