# 🧾 eFactura - Sistema de Facturación Electrónica

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Descripción

eFactura es un sistema completo de facturación electrónica que incluye:

- **Backend API REST** (Flask/Python)
- **Frontend React** con interfaz moderna
- **API para aplicaciones externas** (Contasimple, Sage, etc.)
- **Validación y procesamiento** de facturas
- **Cálculo automático** de totales
- **Tests de accesibilidad** (WCAG 2.1 AA)

## 🚀 Funcionalidades Principales

### **Core System**
- ✅ Gestión completa de facturas (CRUD)
- ✅ Validación automática de datos
- ✅ Cálculo de totales y subtotales
- ✅ Generación de números de factura únicos
- ✅ Base de datos SQLite con SQLAlchemy

### **API para Aplicaciones Externas**
- ✅ **Procesamiento temporal** sin afectar la BD
- ✅ **Validación de datos** antes de procesar
- ✅ **Cálculo de totales** para presupuestos
- ✅ **Migración de datos** desde otros sistemas
- ✅ **Integración** con Contasimple, Sage, etc.

### **Frontend**
- ✅ Interfaz React moderna y responsive
- ✅ Navegación por teclado (accesibilidad)
- ✅ Tests de accesibilidad automatizados
- ✅ Simulador de aplicación externa

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   External Apps │
│   (React)       │◄──►│   (Flask)       │◄──►│   (Contasimple) │
│                 │    │                 │    │   (Sage, etc.)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Database      │
                       │   (SQLite)      │
                       └─────────────────┘
```

## 📁 Estructura del Proyecto

```
efactura/
├── 📂 app/                    # Backend Flask
│   ├── 📂 models/            # Modelos de dominio
│   ├── 📂 services/          # Lógica de negocio
│   └── 📂 utils/             # Utilidades y validadores
├── 📂 frontend/              # Frontend React
│   ├── 📂 public/           # Archivos estáticos
│   │   └── simulator.html   # Simulador externo
│   ├── 📂 src/              # Código React
│   └── 📂 tests/            # Tests de accesibilidad
├── 📄 app.py                 # Punto de entrada del API
├── 📄 swagger.yaml          # Documentación OpenAPI
├── 📄 ejemplo_aplicacion_externa.py  # Ejemplo de integración
└── 📄 README.md             # Esta documentación
```

## 🚀 Instalación y Configuración

### **Prerrequisitos**
- Python 3.8+
- Node.js 16+
- npm o yarn

### **1. Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/efactura.git
cd efactura
```

### **2. Configurar Backend**
```bash
# Crear entorno virtual
python -m venv backend_venv

# Activar entorno (Windows)
backend_venv\Scripts\Activate.ps1

# Activar entorno (Linux/Mac)
source backend_venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### **3. Configurar Frontend**
```bash
cd frontend
npm install
```

### **4. Inicializar Base de Datos**
```bash
python -c "from app import create_app; app = create_app(); app.app_context().push(); from app import db; db.create_all()"
```

## 🎯 Uso

### **Iniciar Backend**
```bash
python app.py
```
**URLs disponibles:**
- API: http://localhost:5000
- Health: http://localhost:5000/health
- Swagger: http://localhost:5000/swagger

### **Iniciar Frontend**
```bash
cd frontend
npm start
```
**URL:** http://localhost:3000

### **Ejecutar Tests de Accesibilidad**
```bash
cd frontend
npm run test:accessibility
```

## 🔗 API Endpoints

### **Core Endpoints**
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Información del API |
| `GET` | `/health` | Estado de salud |
| `GET` | `/api/facturas` | Listar facturas |
| `POST` | `/api/facturas` | Crear factura |

### **External API Endpoints**
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/procesar-factura` | Procesar sin guardar |
| `POST` | `/api/validar-factura` | Validar datos |
| `POST` | `/api/calcular-total` | Calcular totales |

## 🔧 Ejemplos de Uso

### **Procesar Factura Externa**
```python
import requests

factura_externa = {
    "cliente": {
        "nombre": "Empresa Externa S.L.",
        "direccion": "Calle Externa 123, 28001 Madrid",
        "identificacion": "B12345678"
    },
    "items": [
        {
            "descripcion": "Servicio de Consultoría",
            "cantidad": 10,
            "precio": 150.00
        }
    ]
}

response = requests.post(
    "http://localhost:5000/api/procesar-factura",
    json=factura_externa
)

resultado = response.json()
print(f"Factura procesada: {resultado['numero']}")
print(f"Total: €{resultado['total']:.2f}")
```

### **Validar Factura**
```python
response = requests.post(
    "http://localhost:5000/api/validar-factura",
    json=factura_data
)

if response.status_code == 200:
    print("✅ Factura válida")
else:
    print("❌ Factura inválida")
```

### **Calcular Total**
```python
items = [
    {"descripcion": "Producto A", "cantidad": 5, "precio": 25.50},
    {"descripcion": "Servicio B", "cantidad": 2, "precio": 100.00}
]

response = requests.post(
    "http://localhost:5000/api/calcular-total",
    json={"items": items}
)

resultado = response.json()
print(f"Total: €{resultado['total']:.2f}")
```

## 🎯 Casos de Uso

### **Migración desde Contasimple**
1. Exportar facturas desde Contasimple
2. Validar con `/api/validar-factura`
3. Procesar con `/api/procesar-factura`
4. Guardar en sistema propio

### **Integración con Sage**
1. Calcular totales de presupuestos
2. Validar estructura de datos
3. Procesar facturas temporalmente

### **Aplicación Personalizada**
1. Usar validaciones de eFactura
2. Calcular totales automáticamente
3. Integrar con sistemas propios

## 🔒 Seguridad

- ✅ **CORS configurado** para desarrollo
- ✅ **Validación de datos** en todos los endpoints
- ✅ **Procesamiento temporal** para datos externos
- ✅ **Sin persistencia** de datos externos

## 🧪 Testing

### **Tests de Accesibilidad**
```bash
cd frontend
npm run test:accessibility
```

### **Tests de API**
```bash
python -m pytest tests/
```

### **Ejemplo de Aplicación Externa**
```bash
python ejemplo_aplicacion_externa.py
```

## 📚 Documentación

- **[API Externa](API_EXTERNA_README.md)** - Documentación para aplicaciones externas
- **[Swagger](swagger.yaml)** - Documentación OpenAPI completa
- **[Accesibilidad](frontend/ACCESSIBILITY_REPORT.md)** - Reporte de accesibilidad

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Soporte

- **Issues:** [GitHub Issues](https://github.com/tu-usuario/efactura/issues)
- **Documentación:** [Wiki](https://github.com/tu-usuario/efactura/wiki)
- **Email:** support@efactura.com

## 🎉 Agradecimientos

- Flask por el framework web
- React por la interfaz de usuario
- Playwright por los tests de accesibilidad
- SQLAlchemy por el ORM

---

**Desarrollado con ❤️ por el equipo de eFactura** 