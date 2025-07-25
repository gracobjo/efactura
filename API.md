# Documentación de la API - eFactura

Documentación completa de la API REST del sistema eFactura.

## 📋 Información General

- **Base URL**: `http://localhost:5000`
- **Content-Type**: `application/json`
- **Formato de Respuesta**: JSON (excepto PDFs)
- **Autenticación**: No requerida (para desarrollo)

## 🔗 Endpoints Disponibles

### 1. Crear Factura
**POST** `/factura`

Crea una nueva factura y retorna el archivo PDF generado.

#### Request Body
```json
{
  "cliente": {
    "nombre": "Juan Pérez García",
    "direccion": "Calle Mayor 123, 28001 Madrid",
    "identificacion": "12345678A"
  },
  "items": [
    {
      "descripcion": "Servicio de consultoría técnica",
      "cantidad": 2,
      "precio": 150.00
    },
    {
      "descripcion": "Desarrollo de software",
      "cantidad": 1,
      "precio": 500.00
    }
  ]
}
```

#### Validaciones
- **Cliente**:
  - `nombre`: Requerido, mínimo 3 caracteres
  - `direccion`: Requerido, mínimo 10 caracteres
  - `identificacion`: Requerido, formato válido (8+ caracteres)

- **Items**:
  - `descripcion`: Requerido, mínimo 5 caracteres
  - `cantidad`: Requerido, entero positivo
  - `precio`: Requerido, número positivo

#### Response
- **Status**: `200 OK`
- **Content-Type**: `application/pdf`
- **Body**: Archivo PDF de la factura

#### Ejemplo con cURL
```bash
curl -X POST http://localhost:5000/factura \
  -H "Content-Type: application/json" \
  -d '{
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
  }' \
  --output factura.pdf
```

#### Errores Posibles
```json
// 400 Bad Request - Datos inválidos
{
  "message": "Datos del cliente requeridos"
}

// 400 Bad Request - Validación fallida
{
  "message": "La identificación debe tener al menos 8 caracteres"
}

// 500 Internal Server Error
{
  "message": "Error interno: Error al generar PDF"
}
```

---

### 2. Verificar Factura
**GET** `/verificar/{id_factura}`

Obtiene los datos completos de una factura por su ID.

#### Path Parameters
- `id_factura`: ID numérico de la factura

#### Response
```json
{
  "id": 1,
  "numero": "FAC-2024-001",
  "fecha": "2024-01-15",
  "cliente": {
    "nombre": "Juan Pérez García",
    "direccion": "Calle Mayor 123, 28001 Madrid",
    "identificacion": "12345678A"
  },
  "items": [
    {
      "descripcion": "Servicio de consultoría técnica",
      "cantidad": 2,
      "precio_unitario": 150.00,
      "subtotal": 300.00
    },
    {
      "descripcion": "Desarrollo de software",
      "cantidad": 1,
      "precio_unitario": 500.00,
      "subtotal": 500.00
    }
  ],
  "subtotal": 800.00,
  "iva": 168.00,
  "total": 968.00,
  "total_formateado": "968,00 EUR"
}
```

#### Ejemplo con cURL
```bash
curl -X GET http://localhost:5000/verificar/1
```

#### Errores Posibles
```json
// 404 Not Found
{
  "message": "Factura con ID 999 no encontrada"
}
```

---

### 3. Buscar Facturas
**GET** `/facturas`

Busca facturas con filtros opcionales.

#### Query Parameters
- `cliente_nombre` (opcional): Filtrar por nombre del cliente
- `fecha_desde` (opcional): Fecha de inicio (YYYY-MM-DD)
- `fecha_hasta` (opcional): Fecha de fin (YYYY-MM-DD)
- `identificacion` (opcional): Filtrar por identificación del cliente
- `limit` (opcional): Límite de resultados (default: 50)
- `offset` (opcional): Desplazamiento para paginación (default: 0)

#### Response
```json
{
  "facturas": [
    {
      "id": 1,
      "numero": "FAC-2024-001",
      "fecha": "2024-01-15",
      "cliente": {
        "nombre": "Juan Pérez García",
        "identificacion": "12345678A"
      },
      "total": 968.00
    },
    {
      "id": 2,
      "numero": "FAC-2024-002",
      "fecha": "2024-01-16",
      "cliente": {
        "nombre": "María López",
        "identificacion": "87654321B"
      },
      "total": 450.00
    }
  ],
  "total": 2,
  "limit": 50,
  "offset": 0
}
```

#### Ejemplos de Uso
```bash
# Buscar por nombre de cliente
curl "http://localhost:5000/facturas?cliente_nombre=Juan"

# Buscar por rango de fechas
curl "http://localhost:5000/facturas?fecha_desde=2024-01-01&fecha_hasta=2024-01-31"

# Buscar por identificación
curl "http://localhost:5000/facturas?identificacion=12345678A"

# Con paginación
curl "http://localhost:5000/facturas?limit=10&offset=20"
```

---

### 4. Descargar PDF
**GET** `/factura/{id_factura}/pdf`

Descarga el archivo PDF de una factura específica.

#### Path Parameters
- `id_factura`: ID numérico de la factura

#### Response
- **Status**: `200 OK`
- **Content-Type**: `application/pdf`
- **Body**: Archivo PDF de la factura

#### Ejemplo con cURL
```bash
curl -X GET http://localhost:5000/factura/1/pdf --output factura_1.pdf
```

#### Errores Posibles
```json
// 404 Not Found
{
  "message": "Factura con ID 999 no encontrada"
}

// 500 Internal Server Error
{
  "message": "Error al generar PDF: Archivo no encontrado"
}
```

---

### 5. Eliminar Factura
**DELETE** `/factura/{id_factura}`

Elimina una factura y su archivo PDF asociado.

#### Path Parameters
- `id_factura`: ID numérico de la factura

#### Response
```json
{
  "message": "Factura eliminada exitosamente",
  "id": 1
}
```

#### Ejemplo con cURL
```bash
curl -X DELETE http://localhost:5000/factura/1
```

#### Errores Posibles
```json
// 404 Not Found
{
  "message": "Factura con ID 999 no encontrada"
}

// 500 Internal Server Error
{
  "message": "Error al eliminar factura: Error de base de datos"
}
```

---

### 6. Migrar Facturas PDF
**POST** `/migrar-facturas`

Extrae datos de archivos PDF y los migra a la base de datos.

#### Request
- **Content-Type**: `multipart/form-data`
- **Body**: Archivos PDF

#### Response
```json
{
  "message": "Migración completada",
  "archivos_procesados": 3,
  "facturas_creadas": 2,
  "errores": [
    {
      "archivo": "factura_invalida.pdf",
      "error": "No se pudieron extraer datos válidos"
    }
  ],
  "resumen": {
    "exitosos": 2,
    "fallidos": 1
  }
}
```

#### Ejemplo con cURL
```bash
curl -X POST http://localhost:5000/migrar-facturas \
  -F "files=@factura1.pdf" \
  -F "files=@factura2.pdf" \
  -F "files=@factura3.pdf"
```

#### Errores Posibles
```json
// 400 Bad Request - Sin archivos
{
  "message": "No se proporcionaron archivos"
}

// 400 Bad Request - Archivo inválido
{
  "message": "Solo se permiten archivos PDF"
}

// 500 Internal Server Error
{
  "message": "Error al procesar archivos: Error interno"
}
```

---

## 📊 Códigos de Estado HTTP

| Código | Descripción | Uso |
|--------|-------------|-----|
| 200 | OK | Operación exitosa |
| 201 | Created | Recurso creado exitosamente |
| 400 | Bad Request | Datos de entrada inválidos |
| 404 | Not Found | Recurso no encontrado |
| 500 | Internal Server Error | Error interno del servidor |

## 🔍 Filtros de Búsqueda

### Operadores de Fecha
- `fecha_desde`: Fecha de inicio (inclusive)
- `fecha_hasta`: Fecha de fin (inclusive)

### Operadores de Texto
- `cliente_nombre`: Búsqueda parcial por nombre
- `identificacion`: Búsqueda exacta por identificación

### Paginación
- `limit`: Número máximo de resultados (1-100)
- `offset`: Número de resultados a omitir

## 📝 Formatos de Datos

### Fechas
- **Formato**: `YYYY-MM-DD`
- **Ejemplo**: `2024-01-15`

### Moneda
- **Formato**: `XXX,XX EUR`
- **Ejemplo**: `1.234,56 EUR`

### Identificación
- **Formato**: Mínimo 8 caracteres alfanuméricos
- **Ejemplo**: `12345678A`

## 🚨 Manejo de Errores

### Estructura de Error
```json
{
  "message": "Descripción del error",
  "error_code": "ERROR_CODE", // Opcional
  "details": {                // Opcional
    "field": "campo_specifico",
    "value": "valor_invalido"
  }
}
```

### Errores Comunes

#### Validación de Datos
```json
{
  "message": "La identificación debe tener al menos 8 caracteres",
  "error_code": "VALIDATION_ERROR",
  "details": {
    "field": "identificacion",
    "value": "123"
  }
}
```

#### Recurso No Encontrado
```json
{
  "message": "Factura con ID 999 no encontrada",
  "error_code": "NOT_FOUND"
}
```

#### Error Interno
```json
{
  "message": "Error interno del servidor",
  "error_code": "INTERNAL_ERROR"
}
```

## 🔧 Rate Limiting

- **Límite**: 100 requests por minuto por IP
- **Headers de respuesta**:
  - `X-RateLimit-Limit`: Límite de requests
  - `X-RateLimit-Remaining`: Requests restantes
  - `X-RateLimit-Reset`: Tiempo de reset

## 📈 Monitoreo

### Health Check
```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "database": "connected"
}
```

### Métricas
- Tiempo de respuesta promedio
- Número de requests por endpoint
- Tasa de errores
- Uso de memoria y CPU

## 🔐 Seguridad

### Headers de Seguridad
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`

### Validación de Entrada
- Sanitización de datos
- Validación de tipos
- Límites de tamaño de archivo
- Validación de extensiones

## 📚 Ejemplos de Integración

### JavaScript (Fetch API)
```javascript
// Crear factura
async function crearFactura(datosFactura) {
  const response = await fetch('/factura', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(datosFactura)
  });
  
  if (response.ok) {
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'factura.pdf';
    a.click();
  } else {
    const error = await response.json();
    console.error('Error:', error.message);
  }
}
```

### Python (Requests)
```python
import requests

# Crear factura
def crear_factura(datos_factura):
    response = requests.post(
        'http://localhost:5000/factura',
        json=datos_factura
    )
    
    if response.status_code == 200:
        with open('factura.pdf', 'wb') as f:
            f.write(response.content)
        print("Factura creada exitosamente")
    else:
        error = response.json()
        print(f"Error: {error['message']}")

# Verificar factura
def verificar_factura(id_factura):
    response = requests.get(f'http://localhost:5000/verificar/{id_factura}')
    
    if response.status_code == 200:
        factura = response.json()
        print(f"Factura: {factura['numero']}")
        print(f"Total: {factura['total_formateado']}")
    else:
        error = response.json()
        print(f"Error: {error['message']}")
```

### cURL (Bash)
```bash
#!/bin/bash

# Función para crear factura
crear_factura() {
    local datos="$1"
    local output="$2"
    
    curl -X POST http://localhost:5000/factura \
        -H "Content-Type: application/json" \
        -d "$datos" \
        --output "$output"
}

# Función para verificar factura
verificar_factura() {
    local id="$1"
    
    curl -X GET "http://localhost:5000/verificar/$id" \
        -H "Accept: application/json"
}

# Uso
datos='{"cliente":{"nombre":"Test","direccion":"Test 123","identificacion":"12345678A"},"items":[{"descripcion":"Test","cantidad":1,"precio":100}]}'
crear_factura "$datos" "factura_test.pdf"
verificar_factura 1
```

---

*Esta documentación se actualiza regularmente. Para preguntas o sugerencias, abre un issue en el repositorio.* 