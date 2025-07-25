# Guía de Desarrollo - eFactura

Esta guía está dirigida a desarrolladores que quieran contribuir o entender el código del sistema eFactura.

## 🏗️ Arquitectura del Sistema

### Diagrama de Arquitectura General

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Base de       │
│   (React)       │◄──►│   (Flask)       │◄──►│   Datos         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Servicios     │
                       │   (PDF, QR,     │
                       │    Storage)     │
                       └─────────────────┘
```

### Capas de la Aplicación

#### 1. Capa de Presentación (Routes)
- **Responsabilidad**: Manejo de requests HTTP
- **Archivos**: `app/routes/factura_routes.py`
- **Patrones**: Resource-based routing con Flask-RESTful

#### 2. Capa de Servicios
- **Responsabilidad**: Lógica de negocio y servicios externos
- **Archivos**: 
  - `app/services/storage.py` - Persistencia de datos
  - `app/services/pdf_generator.py` - Generación de PDFs
  - `app/services/pdf_extractor.py` - Extracción de datos de PDFs

#### 3. Capa de Modelos
- **Responsabilidad**: Entidades de dominio
- **Archivos**: `app/models/factura.py`
- **Entidades**: Cliente, Item, Factura

#### 4. Capa de Utilidades
- **Responsabilidad**: Funciones auxiliares reutilizables
- **Archivos**:
  - `app/utils/formatters.py` - Formateo de datos
  - `app/utils/validators.py` - Validación de entrada

## 🔧 Configuración del Entorno de Desarrollo

### Requisitos Previos
- Python 3.8+
- Java (para PlantUML)
- Git

### Configuración Inicial
```bash
# 1. Clonar repositorio
git clone <url-repositorio>
cd efactura

# 2. Crear entorno virtual
python -m venv backend_venv
backend_venv\Scripts\activate  # Windows
# source backend_venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp env.example .env
# Editar .env según necesidades

# 5. Ejecutar migración de BD (si es necesario)
python migrate_db.py

# 6. Ejecutar tests
pytest
```

### Variables de Entorno de Desarrollo
```bash
# .env
FLASK_ENV=development
FLASK_DEBUG=true
FLASK_APP=run.py
DATABASE_URL=sqlite:///instance/eFactura.db
SECRET_KEY=dev-secret-key-change-in-production
```

## 📝 Convenciones de Código

### Estilo de Código
- **PEP 8**: Seguir las convenciones de PEP 8
- **Black**: Formateo automático con Black (línea 88)
- **Flake8**: Linting con configuración específica
- **Docstrings**: Usar docstrings en todas las funciones públicas

### Nomenclatura
```python
# Clases: PascalCase
class FacturaResource:
    pass

# Funciones y variables: snake_case
def crear_factura():
    pass

# Constantes: UPPER_SNAKE_CASE
IVA_PORCENTAJE = 0.21

# Archivos: snake_case
factura_routes.py
pdf_generator.py
```

### Estructura de Archivos
```
app/
├── __init__.py          # Factory de aplicación
├── config.py            # Configuración centralizada
├── exceptions.py        # Excepciones personalizadas
├── models/              # Modelos de dominio
├── routes/              # Endpoints de API
├── services/            # Lógica de negocio
└── utils/               # Utilidades
```

## 🧪 Testing

### Estructura de Tests
```
tests/
├── conftest.py          # Configuración de pytest
├── test_factura_api.py  # Tests de integración API
└── test_modelos.py      # Tests unitarios de modelos
```

### Ejecutar Tests
```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=app --cov-report=html

# Tests específicos
pytest tests/test_factura_api.py::test_crear_factura

# Tests con verbose
pytest -v

# Tests con detalle de fallos
pytest -vv --tb=short
```

### Escribir Tests
```python
def test_crear_factura_exitoso(client):
    """Test de creación exitosa de factura"""
    data = {
        "cliente": {
            "nombre": "Test Cliente",
            "direccion": "Test Dirección",
            "identificacion": "12345678A"
        },
        "items": [
            {
                "descripcion": "Test Item",
                "cantidad": 1,
                "precio": 100.00
            }
        ]
    }
    
    response = client.post('/factura', json=data)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/pdf'
```

## 🔍 Debugging

### Logs de Desarrollo
```python
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Usar en código
logger.debug("Valor de variable: %s", variable)
logger.info("Operación completada")
logger.error("Error en operación: %s", error)
```

### Debugger de Python
```python
import pdb; pdb.set_trace()  # Punto de interrupción
# o
breakpoint()  # Python 3.7+
```

### Debugging con VS Code
1. Crear archivo `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "run.py",
                "FLASK_ENV": "development"
            },
            "args": [
                "run",
                "--no-debugger",
                "--no-reload"
            ],
            "jinja": true
        }
    ]
}
```

## 🚀 Despliegue de Desarrollo

### Servidor de Desarrollo
```bash
# Opción 1: Flask run
flask run --debug

# Opción 2: Python directo
python run.py

# Opción 3: Con reload automático
flask run --debug --reload
```

### Base de Datos de Desarrollo
```bash
# SQLite (por defecto)
# Se crea automáticamente en instance/eFactura.db

# Verificar estructura
sqlite3 instance/eFactura.db ".schema"

# Consultar datos
sqlite3 instance/eFactura.db "SELECT * FROM factura;"
```

## 📊 Monitoreo y Métricas

### Métricas de Desarrollo
```python
import time
from functools import wraps

def medir_tiempo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        tiempo = time.time() - inicio
        print(f"{func.__name__} tomó {tiempo:.4f} segundos")
        return resultado
    return wrapper

@medir_tiempo
def funcion_lenta():
    time.sleep(1)
```

### Health Checks
```python
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }
```

## 🔧 Herramientas de Desarrollo

### Pre-commit Hooks
```bash
# Instalar pre-commit
pip install pre-commit

# Configurar hooks
pre-commit install

# Ejecutar manualmente
pre-commit run --all-files
```

### Configuración de pre-commit
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

### Herramientas de Calidad
```bash
# Formateo
black app/ tests/

# Linting
flake8 app/ tests/

# Seguridad
bandit -r app/

# Complejidad
radon cc app/ -a

# Mantenibilidad
radon mi app/
```

## 📚 Documentación

### Generar Documentación
```bash
# Instalar Sphinx
pip install sphinx sphinx-rtd-theme

# Inicializar documentación
sphinx-quickstart docs

# Generar HTML
cd docs && make html
```

### Documentación de API
```python
from flask_restx import Api, Resource, fields

api = Api(app, version='1.0', title='eFactura API',
    description='API para gestión de facturas electrónicas')

@api.doc('crear_factura')
class FacturaResource(Resource):
    @api.expect(factura_model)
    @api.response(200, 'Factura creada exitosamente')
    def post(self):
        """Crea una nueva factura"""
        pass
```

## 🐛 Troubleshooting

### Problemas Comunes

#### Error: "No module named 'flask'"
```bash
# Solución: Activar entorno virtual
backend_venv\Scripts\activate  # Windows
source backend_venv/bin/activate  # Linux/Mac
```

#### Error: "Database is locked"
```bash
# Solución: Cerrar conexiones activas
# Reiniciar aplicación
# Verificar permisos de archivo
```

#### Error: "PlantUML not found"
```bash
# Solución: Instalar Java y PlantUML
java -jar plantuml.jar diagramas/*.puml
```

#### Tests fallando
```bash
# Limpiar cache de pytest
pytest --cache-clear

# Verificar configuración de BD
# Ejecutar tests individualmente
```

## 🔄 Flujo de Trabajo

### 1. Desarrollo de Features
```bash
# Crear rama
git checkout -b feature/nueva-funcionalidad

# Desarrollar
# Hacer commits frecuentes
git add .
git commit -m "feat: agregar nueva funcionalidad"

# Ejecutar tests
pytest

# Verificar calidad
flake8 app/ && black --check app/
```

### 2. Code Review
```bash
# Push a rama
git push origin feature/nueva-funcionalidad

# Crear Pull Request
# Solicitar review
# Abordar comentarios
```

### 3. Merge y Deploy
```bash
# Merge a main
git checkout main
git merge feature/nueva-funcionalidad

# Deploy automático via CI/CD
# Verificar en producción
```

## 📞 Recursos Adicionales

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PlantUML Documentation](http://plantuml.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Black Documentation](https://black.readthedocs.io/)

---

*Esta guía se actualiza regularmente. Para sugerencias o mejoras, abre un issue en el repositorio.* 