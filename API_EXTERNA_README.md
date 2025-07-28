# 🔗 API Externa - eFactura

## 📋 Descripción

Este API permite a **aplicaciones externas** (como Contasimple, Sage, etc.) usar las funcionalidades de eFactura **sin guardar datos en la base de datos del sistema**. Es ideal para:

- ✅ **Migración de datos** desde otros sistemas
- ✅ **Validación de facturas** antes de procesarlas
- ✅ **Cálculo de totales** para presupuestos
- ✅ **Procesamiento temporal** de facturas
- ✅ **Integración** con aplicaciones de terceros

## 🚀 Endpoints Disponibles

### 1. **Procesar Factura Externa** 
`POST /api/procesar-factura`

**Propósito**: Procesa una factura completa sin guardarla en la BD

**Ejemplo**:
```json
{
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
```

**Respuesta**:
```json
{
  "message": "Factura procesada exitosamente",
  "numero": "FAC-20250728-ABC123",
  "cliente": { ... },
  "items": [ ... ],
  "total": 1500.00,
  "fecha": "2025-07-28",
  "procesado_en": "eFactura API"
}
```

### 2. **Validar Factura**
`POST /api/validar-factura`

**Propósito**: Valida los datos de una factura sin procesarla

**Respuesta**:
```json
{
  "message": "Factura válida",
  "cliente_valido": true,
  "items_validos": 2,
  "total_items": 2,
  "errores": []
}
```

### 3. **Calcular Total**
`POST /api/calcular-total`

**Propósito**: Calcula el total de una lista de items

**Ejemplo**:
```json
{
  "items": [
    {
      "descripcion": "Producto A",
      "cantidad": 5,
      "precio": 25.50
    }
  ]
}
```

**Respuesta**:
```json
{
  "message": "Total calculado exitosamente",
  "subtotales": [
    {
      "descripcion": "Producto A",
      "cantidad": 5,
      "precio": 25.50,
      "subtotal": 127.50
    }
  ],
  "total": 127.50,
  "cantidad_items": 1
}
```

## 🔧 Ejemplos de Uso

### **Ejemplo 1: Migración desde Contasimple**

```python
import requests

# Datos de Contasimple
factura_contasimple = {
    "cliente": {
        "nombre": "Cliente Contasimple",
        "direccion": "Calle Contasimple 123",
        "identificacion": "B87654321"
    },
    "items": [
        {"descripcion": "Servicio Contable", "cantidad": 12, "precio": 150.00}
    ]
}

# Procesar sin guardar en BD
response = requests.post(
    "http://localhost:5000/api/procesar-factura",
    json=factura_contasimple
)

resultado = response.json()
print(f"Factura procesada: {resultado['numero']}")
print(f"Total: €{resultado['total']:.2f}")
```

### **Ejemplo 2: Validación de Lote**

```python
# Validar múltiples facturas antes de migrar
facturas = [factura1, factura2, factura3]

for factura in facturas:
    response = requests.post(
        "http://localhost:5000/api/validar-factura",
        json=factura
    )
    
    if response.status_code == 200:
        print("✅ Factura válida")
    else:
        print("❌ Factura inválida")
```

### **Ejemplo 3: Cálculo de Presupuesto**

```python
# Calcular total de presupuesto
items_presupuesto = [
    {"descripcion": "Diseño Web", "cantidad": 1, "precio": 1500.00},
    {"descripcion": "Desarrollo", "cantidad": 20, "precio": 75.00}
]

response = requests.post(
    "http://localhost:5000/api/calcular-total",
    json={"items": items_presupuesto}
)

resultado = response.json()
print(f"Total presupuesto: €{resultado['total']:.2f}")
```

## 🏗️ Arquitectura

```
Aplicación Externa (Contasimple, Sage, etc.)
    ↓ HTTP Request
eFactura API (Flask)
    ↓ Procesamiento
Validación + Cálculos
    ↓ Respuesta JSON
Aplicación Externa
    ↓ Guardar en su propia BD
Base de Datos Externa
```

## 🔒 Seguridad y Privacidad

- ✅ **Sin persistencia**: Los datos no se guardan en la BD de eFactura
- ✅ **Procesamiento temporal**: Solo se procesan en memoria
- ✅ **Validación**: Se validan los datos antes del procesamiento
- ✅ **CORS habilitado**: Permite peticiones desde cualquier origen

## 📁 Archivos del Sistema

| Archivo | Propósito |
|---------|-----------|
| `app.py` | Endpoints principales del API |
| `simulator.html` | Simulador web para probar el API |
| `ejemplo_aplicacion_externa.py` | Ejemplo completo de integración |
| `API_EXTERNA_README.md` | Esta documentación |

## 🚀 Cómo Usar

### **1. Iniciar el Servidor**
```bash
python app.py
```

### **2. Probar con el Simulador**
Abrir `frontend/public/simulator.html` en el navegador

### **3. Usar desde Aplicación Externa**
```python
python ejemplo_aplicacion_externa.py
```

## 🎯 Casos de Uso Reales

### **Contasimple → eFactura**
- Migrar facturas existentes
- Validar antes de la migración
- Procesar sin afectar la BD

### **Sage → eFactura**
- Calcular totales de presupuestos
- Validar estructura de datos
- Procesar facturas temporalmente

### **Aplicación Personalizada**
- Integrar con sistemas propios
- Usar validaciones de eFactura
- Calcular totales automáticamente

## 🔧 Configuración

### **URLs del API**
- **Base**: http://localhost:5000
- **Health**: http://localhost:5000/health
- **Procesar**: http://localhost:5000/api/procesar-factura
- **Validar**: http://localhost:5000/api/validar-factura
- **Calcular**: http://localhost:5000/api/calcular-total

### **Headers Requeridos**
```http
Content-Type: application/json
```

## 🎉 Ventajas

1. **Flexibilidad**: Cualquier aplicación puede conectarse
2. **Seguridad**: No se guardan datos externos
3. **Validación**: Usa las mismas reglas de eFactura
4. **Escalabilidad**: Múltiples aplicaciones simultáneas
5. **Simplicidad**: API REST estándar

## 📞 Soporte

Para más información o soporte técnico, consulta la documentación completa del proyecto eFactura. 