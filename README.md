# eFactura - Sistema de Facturación Electrónica

Sistema completo de facturación electrónica con generación de PDFs, códigos QR de verificación y migración de facturas existentes.

## 🚀 Características

- **Generación de facturas PDF** con códigos QR de verificación
- **Migración de facturas PDF existentes** a la base de datos
- **API REST completa** para gestión de facturas
- **Búsqueda avanzada** con múltiples filtros
- **Validación robusta** de datos de entrada
- **Manejo de errores centralizado**
- **Configuración modular** por entornos
- **Código limpio y mantenible**
- **Documentación UML completa**

## 📁 Estructura del Proyecto

```
efactura/
├── app/
│   ├── __init__.py              # Factory de la aplicación Flask
│   ├── config.py                # Configuración centralizada
│   ├── exceptions.py            # Excepciones personalizadas
│   ├── models/
│   │   └── factura.py           # Modelos de dominio
│   ├── routes/
│   │   └── factura_routes.py    # Endpoints de la API
│   ├── services/
│   │   ├── storage.py           # Capa de persistencia
│   │   ├── pdf_generator.py     # Generación de PDFs
│   │   └── pdf_extractor.py     # Extracción de datos de PDFs
│   └── utils/
│       ├── formatters.py        # Utilidades de formateo
│       └── validators.py        # Validación de datos
├── diagramas/                   # Diagramas UML del sistema
│   ├── 01_diagrama_casos_uso.puml
│   ├── 02_diagrama_clases.puml
│   ├── 03_diagrama_secuencia.puml
│   ├── 04_diagrama_secuencia_verificacion.puml
│   ├── 05_diagrama_actividad.puml
│   ├── 06_diagrama_estado.puml
│   ├── 07_diagrama_componentes.puml
│   ├── 08_diagrama_despliegue.puml
│   └── README.md                # Documentación de diagramas
├── tests/                       # Tests unitarios e integración
├── frontend/                    # Interfaz web (React)
├── requirements.txt             # Dependencias Python
├── run.py                       # Punto de entrada
├── migrate_db.py                # Script de migración de BD
├── env.example                  # Variables de entorno de ejemplo
├── pyproject.toml               # Configuración de herramientas
└── README.md                    # Este archivo
```

## 📊 Diagramas UML

El proyecto incluye una documentación UML completa en el directorio `diagramas/`:

### Diagramas Esenciales
- **Diagrama de Casos de Uso**: Interacciones entre usuarios y sistema
- **Diagrama de Clases**: Estructura de clases y relaciones
- **Diagrama de Secuencia**: Flujo de interacciones (Crear/Verificar Factura)
- **Diagrama de Actividad**: Flujo de trabajo del sistema

### Diagramas Opcionales
- **Diagrama de Estado**: Estados de una factura
- **Diagrama de Componentes**: Arquitectura de componentes
- **Diagrama de Despliegue**: Infraestructura y despliegue

### Visualizar Diagramas
```bash
# Opción 1: PlantUML Online
# Ve a http://www.plantuml.com/plantuml/uml/ y pega el contenido .puml

# Opción 2: PlantUML Local
java -jar plantuml.jar diagramas/*.puml

# Opción 3: VS Code con extensión PlantUML
# Instala "PlantUML" y usa Ctrl+Shift+P > "PlantUML: Preview"
```

## 🛠️ Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd efactura
   ```

2. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   ```bash
   # Copiar archivo de ejemplo
   cp env.example .env
   
   # Editar variables según entorno
   export FLASK_ENV=development
   export FLASK_APP=run.py
   ```

5. **Migrar base de datos (si es necesario):**
   ```bash
   python migrate_db.py
   ```

6. **Ejecutar la aplicación:**
   ```bash
   python run.py
   ```

## 📚 API Endpoints

### Crear Factura
```http
POST /factura
Content-Type: application/json

{
  "cliente": {
    "nombre": "Juan Pérez",
    "direccion": "Calle Mayor 123",
    "identificacion": "12345678A"
  },
  "items": [
    {
      "descripcion": "Servicio de consultoría",
      "cantidad": 2,
      "precio": 100.00
    }
  ]
}
```

**Respuesta:** Archivo PDF de la factura generada

### Verificar Factura
```http
GET /verificar/{id_factura}
```

**Respuesta:**
```json
{
  "id": 1,
  "numero": "FAC-2024-001",
  "fecha": "2024-01-15",
  "cliente": {
    "nombre": "Juan Pérez",
    "direccion": "Calle Mayor 123",
    "identificacion": "12345678A"
  },
  "items": [...],
  "total": "242,00 EUR"
}
```

### Buscar Facturas
```http
GET /facturas?cliente_nombre=Juan&fecha_desde=2024-01-01&fecha_hasta=2024-12-31
```

**Parámetros opcionales:**
- `cliente_nombre`: Filtrar por nombre del cliente
- `fecha_desde`: Fecha de inicio (YYYY-MM-DD)
- `fecha_hasta`: Fecha de fin (YYYY-MM-DD)
- `identificacion`: Filtrar por identificación del cliente

### Descargar PDF
```http
GET /factura/{id_factura}/pdf
```

### Eliminar Factura
```http
DELETE /factura/{id_factura}
```

### Migrar Facturas PDF
```http
POST /migrar-facturas
Content-Type: multipart/form-data

files: [archivos PDF]
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=app --cov-report=html

# Tests específicos
pytest tests/test_factura_api.py
pytest tests/test_modelos.py

# Verificar calidad del código
flake8 app/ tests/
black --check app/ tests/
bandit -r app/
```

## 🔧 Configuración

El proyecto soporta múltiples entornos de configuración:

### Variables de Entorno
```bash
# Flask
FLASK_ENV=development|production|testing
FLASK_APP=run.py
FLASK_DEBUG=true|false

# Base de Datos
DATABASE_URL=sqlite:///instance/eFactura.db
POSTGRES_URL=postgresql://user:pass@localhost/efactura

# Servidor
HOST=0.0.0.0
PORT=5000

# Seguridad
SECRET_KEY=your-secret-key
MAX_CONTENT_LENGTH=16777216

# Facturación
IVA_PORCENTAJE=0.21
BASE_URL_VERIFICACION=http://localhost:5000/verificar/
```

### Configuraciones por Entorno
- **Development**: Configuración para desarrollo local con SQLite
- **Production**: Configuración para producción con PostgreSQL
- **Testing**: Configuración para tests con base de datos en memoria

## 🏗️ Arquitectura

### Principios de Diseño

1. **Separación de Responsabilidades**: Cada módulo tiene una responsabilidad específica
2. **Inyección de Dependencias**: Configuración centralizada y modular
3. **Manejo de Errores**: Excepciones personalizadas y manejo consistente
4. **Validación**: Validación robusta de datos de entrada
5. **Código Limpio**: Estructura clara y mantenible

### Capas de la Aplicación

- **Routes**: Manejo de requests HTTP y respuestas
- **Services**: Lógica de negocio y servicios externos
- **Models**: Modelos de dominio y entidades
- **Utils**: Utilidades y helpers reutilizables
- **Storage**: Persistencia de datos y mapeo objeto-relacional

### Patrones Utilizados

- **Factory Pattern**: Creación de aplicación Flask
- **Repository Pattern**: Acceso a datos a través de Storage
- **Strategy Pattern**: Diferentes configuraciones por entorno
- **Exception Handling**: Manejo centralizado de errores

## 🚀 Despliegue

### Desarrollo Local
```bash
python run.py
```

### Producción con Gunicorn
```bash
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 run:app
```

### Docker (Recomendado)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

### CI/CD Pipeline
El proyecto incluye GitHub Actions para:
- Tests automáticos en múltiples versiones de Python
- Verificación de calidad de código (flake8, black, bandit)
- Análisis de seguridad de dependencias
- Despliegue automático

## 📝 Mejoras Implementadas

### Antes vs Después

**Antes:**
- ❌ Código duplicado en múltiples archivos
- ❌ Configuración hardcodeada
- ❌ Manejo de errores inconsistente
- ❌ Validación básica
- ❌ Archivos muy largos y complejos
- ❌ Falta de documentación técnica

**Después:**
- ✅ Configuración centralizada (`app/config.py`)
- ✅ Utilidades reutilizables (`app/utils/`)
- ✅ Excepciones personalizadas (`app/exceptions.py`)
- ✅ Validación robusta (`app/utils/validators.py`)
- ✅ Separación de responsabilidades
- ✅ Código más limpio y mantenible
- ✅ Manejo de errores consistente
- ✅ Documentación UML completa
- ✅ CI/CD pipeline automatizado
- ✅ Tests con cobertura

## 🔍 Monitoreo y Logs

### Logs de Aplicación
```python
import logging
logging.info("Factura creada exitosamente")
logging.error("Error al procesar PDF")
```

### Métricas Recomendadas
- Número de facturas creadas por día
- Tiempo de respuesta de la API
- Tasa de errores por endpoint
- Uso de almacenamiento

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Ejecuta los tests: `pytest`
4. Verifica la calidad: `flake8 app/ && black --check app/`
5. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
6. Push a la rama (`git push origin feature/AmazingFeature`)
7. Abre un Pull Request

### Guías de Contribución
- Sigue las convenciones de código existentes
- Agrega tests para nuevas funcionalidades
- Actualiza la documentación según sea necesario
- Verifica que todos los tests pasen antes del PR

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Soporte

Para soporte técnico o preguntas:
- Abre un issue en GitHub
- Revisa la documentación en `diagramas/README.md`
- Consulta los diagramas UML para entender la arquitectura

---

*Desarrollado con ❤️ usando Flask, SQLAlchemy y PlantUML* 