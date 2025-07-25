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
├── tests/                       # Tests unitarios e integración
├── frontend/                    # Interfaz web (React)
├── requirements.txt             # Dependencias Python
├── run.py                       # Punto de entrada
└── README.md                    # Este archivo
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
   export FLASK_ENV=development
   export FLASK_APP=run.py
   ```

5. **Ejecutar la aplicación:**
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

### Verificar Factura
```http
GET /verificar/{id_factura}
```

### Buscar Facturas
```http
GET /facturas?cliente_nombre=Juan&fecha_desde=2024-01-01
```

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
pytest --cov=app

# Tests específicos
pytest tests/test_factura_api.py
```

## 🔧 Configuración

El proyecto soporta múltiples entornos de configuración:

- **Development**: Configuración para desarrollo local
- **Production**: Configuración para producción
- **Testing**: Configuración para tests

Las configuraciones se manejan en `app/config.py` y se pueden personalizar según necesidades.

## 🏗️ Arquitectura

### Principios de Diseño

1. **Separación de Responsabilidades**: Cada módulo tiene una responsabilidad específica
2. **Inyección de Dependencias**: Configuración centralizada y modular
3. **Manejo de Errores**: Excepciones personalizadas y manejo consistente
4. **Validación**: Validación robusta de datos de entrada
5. **Código Limpio**: Estructura clara y mantenible

### Capas de la Aplicación

- **Routes**: Manejo de requests HTTP
- **Services**: Lógica de negocio y servicios externos
- **Models**: Modelos de dominio
- **Utils**: Utilidades y helpers
- **Storage**: Persistencia de datos

## 🚀 Despliegue

### Desarrollo Local
```bash
python run.py
```

### Producción
```bash
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 📝 Mejoras Implementadas

### Antes vs Después

**Antes:**
- Código duplicado en múltiples archivos
- Configuración hardcodeada
- Manejo de errores inconsistente
- Validación básica
- Archivos muy largos y complejos

**Después:**
- ✅ Configuración centralizada (`app/config.py`)
- ✅ Utilidades reutilizables (`app/utils/`)
- ✅ Excepciones personalizadas (`app/exceptions.py`)
- ✅ Validación robusta (`app/utils/validators.py`)
- ✅ Separación de responsabilidades
- ✅ Código más limpio y mantenible
- ✅ Manejo de errores consistente
- ✅ Documentación mejorada

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles. 