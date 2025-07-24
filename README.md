[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gracobjo/efactura/blob/main/demo_colab.ipynb)

# eFactura

Sistema de facturación electrónica completo con backend en Python (Flask) y frontend en React.

---

## 🧾 Cómo se genera y verifica una factura electrónica

### 1. Generación de la factura (PDF con QR)

- **Paso 1:** Envía los datos de la factura a la API REST (`/factura`) mediante una petición POST con un JSON como este:

  ```json
  {
    "cliente": {
      "nombre": "Carlos Ruiz",
      "direccion": "Calle Nueva 456",
      "identificacion": "11223344C"
    },
    "items": [
      {"descripcion": "Producto Z", "cantidad": 2, "precio_unitario": 150.0},
      {"descripcion": "Servicio Y", "cantidad": 1, "precio_unitario": 300.0}
    ]
  }
  ```

- **Paso 2:** La API genera:
  - Un registro en la base de datos con los datos de la factura.
  - Un PDF en `instance/facturas/` y lo devuelve como respuesta (descarga directa).
  - El PDF incluye:
    - Datos del cliente y los ítems
    - Desglose de total sin IVA, IVA y total con IVA
    - Un **código QR** que contiene un JSON con los datos mínimos requeridos por el Real Decreto 1007/2023 (NIF emisor, número, fecha, total, hash, URL de verificación)
    - Una leyenda: `Factura verificable en http://localhost:5000/verificar/<id_factura>`

- **Ejemplo de comando en PowerShell:**
  ```powershell
  Invoke-WebRequest -Uri http://localhost:5000/factura `
    -Method POST `
    -ContentType "application/json" `
    -InFile "factura.json" `
    -OutFile "factura.pdf"
  ```

### 2. Verificación de la factura

- **Paso 1:** Escanea el QR del PDF con tu móvil o una app de QR.
- **Paso 2:** El QR contiene un JSON con los datos clave y la URL de verificación.
- **Paso 3:** Al abrir la URL (por ejemplo, `http://localhost:5000/verificar/1`), la API responde con los datos básicos de la factura, incluyendo:
  - Número de factura
  - Fecha
  - Cliente (nombre e identificación)
  - Total sin IVA
  - IVA
  - Total con IVA

- **Ejemplo de respuesta:**
  ```json
  {
    "numero": "FAC-20250724-9958C5",
    "fecha": "2025-07-24",
    "cliente": {
      "nombre": "Juan Pérez",
      "identificacion": "12345678A"
    },
    "total": 250.0,
    "iva": 52.5,
    "total_con_iva": 302.5
  }
  ```

- **Leyenda en el PDF:**
  > Factura verificable en http://localhost:5000/verificar/1

---

## 🚀 Características

- **Backend API REST** con Flask para crear y verificar facturas
- **Frontend React** con interfaz moderna y responsive
- **Generación de PDF** con datos, ítems, total, IVA y código QR
- **Almacenamiento en SQLite** con SQLAlchemy
- **Análisis de facturación** con Pandas y Matplotlib
- **Código QR** para verificación de facturas

---

## 📋 Tabla de Contenidos

- [Instalación](#instalación)
- [Manual de Usuario](#manual-de-usuario)
- [Manual de Desarrollador](#manual-de-desarrollador)
- [API REST](#api-rest)
- [Análisis de Datos](#análisis-de-datos)
- [CI/CD y Despliegue](#cicd-y-despliegue)
- [Despliegue](#despliegue)

---

## 🛠️ Instalación

### Requisitos Previos
- Python 3.8+
- Node.js 14+
- npm o yarn

### Backend (Flask)
```bash
# Clonar el repositorio
git clone <url-del-repo>
cd eFactura

# Instalar dependencias Python
pip install -r requirements.txt

# Inicializar base de datos
python run.py
python poblar_db.py
```

### Frontend (React)
```bash
# Instalar dependencias
cd frontend
npm install

# Configurar API (opcional)
echo "REACT_APP_API_URL=http://localhost:5000" > .env
```

---

## 👤 Manual de Usuario

### Iniciar la Aplicación

1. **Backend:**
   ```bash
   python run.py
   ```
   El servidor estará en `http://localhost:5000`

2. **Frontend:**
   ```bash
   cd frontend
   npm start
   ```
   La aplicación estará en `http://localhost:3000`

### 🚀 Iniciar la Aplicación

**IMPORTANTE:** Necesitas tener **ambos servicios** ejecutándose:

1. **Backend (API):** Debe estar en `http://localhost:5000`
2. **Frontend (Interfaz):** Debe estar en `http://localhost:3000`

#### Opción 1: Usar solo la API (Recomendado para pruebas rápidas)

Si solo quieres probar la API sin el frontend:

```bash
# Solo ejecuta el backend
python run.py
```

Luego usa Postman, curl o PowerShell para hacer peticiones a `http://localhost:5000/factura`

#### Opción 2: Usar la interfaz web completa

1. **Terminal 1 - Backend:**
   ```bash
   python run.py
   ```

2. **Terminal 2 - Frontend:**
   ```bash
   cd frontend
   npm start
   ```

3. **Abrir navegador:** `http://localhost:3000`

### 📝 Crear una Factura

#### Con la interfaz web (puerto 3000):
1. Abre el navegador en `http://localhost:3000`
2. Haz clic en la pestaña **"Crear Factura"**
3. Completa los datos del cliente:
   - Nombre
   - Dirección
   - Identificación
4. Agrega los ítems de la factura:
   - Descripción del producto/servicio
   - Cantidad
   - Precio unitario
5. Haz clic en **"Agregar Ítem"** si necesitas más productos
6. Haz clic en **"Crear Factura"**
7. El PDF se descargará automáticamente

#### Con la API directamente (puerto 5000):
Ver ejemplos más abajo con Postman, curl o PowerShell.

### 🔍 Verificar una Factura

#### Con la interfaz web:
1. Haz clic en la pestaña **"Verificar Factura"**
2. Ingresa el ID de la factura
3. Haz clic en **"Verificar"**
4. Se mostrarán los datos básicos de la factura

#### Con la API directamente:
```bash
curl http://localhost:5000/verificar/1
```

### Análisis de Facturación

```bash
python analisis_facturas.py
```
Esto mostrará:
- Total facturado por mes
- Facturación por cliente
- Gráfico de barras

### 🔧 Solución de Problemas

#### ❌ Error: "Cannot connect to localhost:3000"
**Causa:** El frontend no está ejecutándose
**Solución:**
```bash
cd frontend
npm install  # Si no has instalado las dependencias
npm start
```

#### ❌ Error: "Cannot connect to localhost:5000"
**Causa:** El backend no está ejecutándose
**Solución:**
```bash
python run.py
```

#### ❌ Error: "npm command not found"
**Causa:** Node.js no está instalado
**Solución:** Instala Node.js desde https://nodejs.org/

#### ❌ Error: "Module not found" en Python
**Causa:** Dependencias no instaladas
**Solución:**
```bash
pip install -r requirements.txt
```

#### ✅ Verificar que todo funciona:
1. **Backend:** `http://localhost:5000/verificar/1` (debe devolver JSON o 404)
2. **Frontend:** `http://localhost:3000` (debe mostrar la interfaz)

---

## 📨 Ejemplo rápido: Crear una factura y descargar el PDF con Postman

1. Abre Postman y crea una nueva petición:
   - **Método:** POST
   - **URL:** `http://localhost:5000/factura`

2. Ve a la pestaña **Body** y selecciona **raw** y **JSON**. Pega el siguiente contenido:

   ```json
   {
     "cliente": {
       "nombre": "Carlos Ruiz",
       "direccion": "Calle Nueva 456",
       "identificacion": "11223344C"
     },
     "items": [
       {"descripcion": "Producto Z", "cantidad": 2, "precio_unitario": 150.0},
       {"descripcion": "Servicio Y", "cantidad": 1, "precio_unitario": 300.0}
     ]
   }
   ```

3. Haz clic en **Send**.

4. Cuando recibas la respuesta (el PDF), haz clic en **Save Response > Save to a file...** y guárdalo como `factura.pdf`.

¡Listo! Así puedes crear y descargar facturas fácilmente usando Postman.

---

## 🖥️ Ejemplo rápido: Crear una factura y descargar el PDF en PowerShell

1. Crea un archivo `factura.json` con el contenido de la factura:

   ```json
   {
     "cliente": {
       "nombre": "Carlos Ruiz",
       "direccion": "Calle Nueva 456",
       "identificacion": "11223344C"
     },
     "items": [
       {"descripcion": "Producto Z", "cantidad": 2, "precio_unitario": 150.0},
       {"descripcion": "Servicio Y", "cantidad": 1, "precio_unitario": 300.0}
     ]
   }
   ```

2. Ejecuta este comando en PowerShell:

   ```powershell
   Invoke-WebRequest -Uri http://localhost:5000/factura `
     -Method POST `
     -ContentType "application/json" `
     -InFile "factura.json" `
     -OutFile "factura.pdf"
   ```

Esto enviará la factura a la API y descargará el PDF generado como `factura.pdf` en tu carpeta actual.

---

## 👨‍💻 Manual de Desarrollador

### Estructura del Proyecto

```
eFactura/
├── app/                    # Backend Flask
│   ├── __init__.py        # Configuración de la app
│   ├── models/            # Modelos de datos
│   │   └── factura.py     # Clases Cliente, Item, Factura
│   ├── routes/            # Endpoints de la API
│   │   └── factura_routes.py
│   └── services/          # Lógica de negocio
│       ├── pdf_generator.py
│       ├── qr_generator.py
│       └── storage.py
├── frontend/              # Frontend React
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── App.js
│   │   └── api.js         # Configuración de API
│   └── package.json
├── instance/              # Base de datos y PDFs
├── requirements.txt       # Dependencias Python
├── run.py                # Script de inicio
├── poblar_db.py          # Datos de ejemplo
└── analisis_facturas.py  # Análisis con Pandas
```

### Tecnologías Utilizadas

**Backend:**
- Flask (Framework web)
- Flask-RESTful (API REST)
- SQLAlchemy (ORM)
- fpdf (Generación de PDF)
- qrcode (Códigos QR)
- Pandas (Análisis de datos)

**Frontend:**
- React 18
- Axios (Cliente HTTP)
- CSS3 (Estilos responsive)

### Desarrollo Local

1. **Configurar entorno de desarrollo:**
   ```bash
   # Backend
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Frontend
   cd frontend
   npm install
   ```

2. **Ejecutar en modo desarrollo:**
   ```bash
   # Terminal 1 - Backend
   python run.py
   
   # Terminal 2 - Frontend
   cd frontend
   npm start
   ```

3. **Acceder a la aplicación:**
   - Frontend: `http://localhost:3000`
   - API: `http://localhost:5000`

### Modificar el Backend

**Agregar un nuevo endpoint:**
1. Edita `app/routes/factura_routes.py`
2. Crea una nueva clase que herede de `Resource`
3. Registra el endpoint en `app/__init__.py`

**Modificar modelos:**
1. Edita `app/models/factura.py`
2. Actualiza `app/services/storage.py` si es necesario
3. Ejecuta migraciones si usas Flask-Migrate

### Modificar el Frontend

**Agregar un nuevo componente:**
1. Crea el archivo en `frontend/src/components/`
2. Importa y usa en `App.js`
3. Agrega estilos en `App.css`

**Modificar la API:**
1. Edita `frontend/src/api.js`
2. Actualiza los componentes que usen la API

### Testing

```bash
# Backend (cuando implementes tests)
python -m pytest

# Frontend
cd frontend
npm test
```

### Build para Producción

```bash
# Frontend
cd frontend
npm run build

# Backend
# Usar gunicorn u otro servidor WSGI
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

---

## 🔌 API REST

### Endpoints Disponibles

#### POST /factura
Crea una nueva factura y devuelve el PDF.

**Request:**
```json
{
  "cliente": {
    "nombre": "Carlos Ruiz",
    "direccion": "Calle Nueva 456",
    "identificacion": "11223344C"
  },
  "items": [
    {"descripcion": "Producto Z", "cantidad": 2, "precio_unitario": 150.0},
    {"descripcion": "Servicio Y", "cantidad": 1, "precio_unitario": 300.0}
  ]
}
```

**Response:** PDF file

#### GET /verificar/{id_factura}
Verifica una factura por su ID.

**Response:**
```json
{
  "numero": "FAC-20240601-XXXXXX",
  "fecha": "2024-06-01",
  "cliente": {
    "nombre": "Carlos Ruiz",
    "identificacion": "11223344C"
  },
  "total": 600.0
}
```

### Especificación Swagger/OpenAPI

```yaml
openapi: 3.0.0
info:
  title: eFactura API
  version: 1.0.0
paths:
  /factura:
    post:
      summary: Crear una nueva factura y devolver el PDF generado
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                cliente:
                  type: object
                  properties:
                    nombre:
                      type: string
                    direccion:
                      type: string
                    identificacion:
                      type: string
                  required: [nombre, direccion, identificacion]
                items:
                  type: array
                  items:
                    type: object
                    properties:
                      descripcion:
                        type: string
                      cantidad:
                        type: integer
                      precio_unitario:
                        type: number
                    required: [descripcion, cantidad, precio_unitario]
              required: [cliente, items]
      responses:
        '200':
          description: PDF generado
          content:
            application/pdf:
              schema:
                type: string
                format: binary
        '400':
          description: Datos inválidos
  /verificar/{id_factura}:
    get:
      summary: Verificar una factura por su ID
      parameters:
        - in: path
          name: id_factura
          schema:
            type: integer
          required: true
          description: ID de la factura
      responses:
        '200':
          description: Datos básicos de la factura
          content:
            application/json:
              schema:
                type: object
                properties:
                  numero:
                    type: string
                  fecha:
                    type: string
                  cliente:
                    type: object
                    properties:
                      nombre:
                        type: string
                      identificacion:
                        type: string
                  total:
                    type: number
        '404':
          description: Factura no encontrada
```

---

## 📊 Análisis de Datos

### Script de Análisis

```bash
python analisis_facturas.py
```

**Funcionalidades:**
- Total facturado por mes
- Facturación por cliente
- Gráfico de barras con matplotlib

### Personalizar Análisis

Edita `analisis_facturas.py` para agregar:
- Filtros por fecha
- Análisis de tendencias
- Exportación a Excel
- Más tipos de gráficos

---

## 🌐 Endpoints de la API REST

| Método | Endpoint                                 | Descripción                                      |
|--------|------------------------------------------|--------------------------------------------------|
| POST   | /factura                                 | Crear una factura y devolver el PDF generado     |
| GET    | /verificar/{id_factura}                  | Verificar una factura por su ID                  |
| GET    | /facturas                                | Buscar y listar facturas con filtros avanzados   |
| GET    | /factura/{id_factura}/pdf                | Descargar el PDF de una factura por su ID        |
| DELETE | /factura/{id_factura}                    | Eliminar una factura por su ID                   |

### 📝 Ejemplos de uso para cada endpoint

#### 1. POST /factura - Crear factura

**Request:**
```bash
curl -X POST http://localhost:5000/factura \
  -H "Content-Type: application/json" \
  -d '{
    "cliente": {
      "nombre": "Carlos Ruiz",
      "direccion": "Calle Nueva 456",
      "identificacion": "11223344C"
    },
    "items": [
      {"descripcion": "Producto Z", "cantidad": 2, "precio_unitario": 150.0},
      {"descripcion": "Servicio Y", "cantidad": 1, "precio_unitario": 300.0}
    ]
  }'
```

**Response:** Archivo PDF (Content-Type: application/pdf)

#### 2. GET /verificar/{id_factura} - Verificar factura

**Request:**
```bash
curl -X GET http://localhost:5000/verificar/1
```

**Response:**
```json
{
  "id": 1,
  "numero": "FAC-20241201-ABC123",
  "fecha": "2024-12-01T10:30:00",
  "cliente": {
    "nombre": "Carlos Ruiz",
    "direccion": "Calle Nueva 456",
    "identificacion": "11223344C"
  },
  "items": [
    {
      "descripcion": "Producto Z",
      "cantidad": 2,
      "precio_unitario": 150.0,
      "subtotal": 300.0
    },
    {
      "descripcion": "Servicio Y",
      "cantidad": 1,
      "precio_unitario": 300.0,
      "subtotal": 300.0
    }
  ],
  "total": 600.0,
  "iva": 126.0,
  "total_con_iva": 726.0
}
```

#### 3. GET /facturas - Buscar facturas

**Request:**
```bash
# Buscar por nombre de cliente
curl -X GET "http://localhost:5000/facturas?cliente_nombre=Carlos"

# Buscar por rango de fechas
curl -X GET "http://localhost:5000/facturas?fecha_desde=2024-01-01&fecha_hasta=2024-12-31"

# Buscar por monto mínimo
curl -X GET "http://localhost:5000/facturas?monto_minimo=500"

# Combinar filtros
curl -X GET "http://localhost:5000/facturas?cliente_nombre=Carlos&monto_minimo=500&fecha_desde=2024-01-01"
```

**Response:**
```json
[
  {
    "id": 1,
    "numero": "FAC-20241201-ABC123",
    "fecha": "2024-12-01T10:30:00",
    "cliente": {
      "nombre": "Carlos Ruiz",
      "direccion": "Calle Nueva 456",
      "identificacion": "11223344C"
    },
    "total": 726.0
  },
  {
    "id": 2,
    "numero": "FAC-20241201-DEF456",
    "fecha": "2024-12-01T14:20:00",
    "cliente": {
      "nombre": "Carlos López",
      "direccion": "Av. Principal 789",
      "identificacion": "99887766D"
    },
    "total": 550.0
  }
]
```

#### 4. GET /factura/{id_factura}/pdf - Descargar PDF

**Request:**
```bash
curl -X GET http://localhost:5000/factura/1/pdf -o factura_1.pdf
```

**Response:** Archivo PDF (Content-Type: application/pdf)

#### 5. DELETE /factura/{id_factura} - Eliminar factura

**Request:**
```bash
curl -X DELETE http://localhost:5000/factura/1
```

**Response:**
```json
{
  "mensaje": "Factura eliminada correctamente",
  "id_eliminado": 1
}
```

### 🔍 Parámetros de búsqueda disponibles

Para el endpoint `GET /facturas`, puedes usar estos filtros:

| Parámetro      | Tipo   | Descripción                    | Ejemplo                    |
|----------------|--------|--------------------------------|----------------------------|
| cliente_nombre | string | Buscar por nombre del cliente  | `?cliente_nombre=Juan`     |
| fecha_desde    | date   | Fecha de inicio (YYYY-MM-DD)   | `?fecha_desde=2024-01-01`  |
| fecha_hasta    | date   | Fecha de fin (YYYY-MM-DD)      | `?fecha_hasta=2024-12-31`  |
| monto_minimo   | float  | Monto mínimo de la factura     | `?monto_minimo=100.0`      |
| monto_maximo   | float  | Monto máximo de la factura     | `?monto_maximo=1000.0`     |
| limit          | int    | Límite de resultados           | `?limit=10`               |
| offset         | int    | Desplazamiento de resultados   | `?offset=20`              |

### ❌ Códigos de error comunes

| Código | Descripción                    | Causa típica                    |
|--------|--------------------------------|---------------------------------|
| 400    | Bad Request                    | JSON malformado o datos faltantes |
| 404    | Not Found                     | Factura no encontrada           |
| 500    | Internal Server Error          | Error interno del servidor      |

**Ejemplo de error 404:**
```json
{
  "error": "Factura no encontrada",
  "mensaje": "No se encontró la factura con ID: 999"
}
```

---

## 📝 Notas

- Cambia las URLs base según tu entorno de despliegue
- Configura CORS en el backend si el frontend está en otro dominio
- Considera usar una base de datos PostgreSQL para producción
- Implementa autenticación para entornos de producción

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 

---

## 🔄 CI/CD y Despliegue

### 🚀 Continuous Integration/Continuous Deployment

El proyecto incluye un pipeline completo de CI/CD configurado con GitHub Actions:

#### ✅ **Tests Automatizados**
- **Tests unitarios** con pytest
- **Tests de integración** para la API
- **Cobertura de código** con reportes HTML y XML
- **Múltiples versiones de Python** (3.8, 3.9, 3.10, 3.11)

#### 🔍 **Análisis de Código**
- **Linting** con flake8
- **Formateo** con black
- **Análisis de seguridad** con bandit y safety
- **Reportes de calidad** automáticos

#### 🏗️ **Build y Deploy**
- **Build automático** en cada push a main
- **Artefactos** generados automáticamente
- **Deploy a staging** (configurable)
- **Notificaciones** de éxito/fallo

#### 📦 **Gestión de Dependencias**
- **Dependabot** para actualizaciones automáticas
- **Seguridad** de dependencias monitoreada
- **Pull requests** automáticos para actualizaciones

### 🛠️ **Configuración Local de CI/CD**

Para ejecutar las herramientas de CI/CD localmente:

```bash
# Instalar herramientas de desarrollo
pip install pytest-cov flake8 black bandit safety

# Ejecutar tests con cobertura
pytest --cov=app --cov-report=html

# Linting
flake8 .

# Formateo de código
black .

# Análisis de seguridad
bandit -r app/
safety check
```

### 📊 **Badges de Estado**

Una vez configurado, puedes agregar estos badges a tu README:

```markdown
![Tests](https://github.com/gracobjo/efactura/workflows/CI%2FCD%20Pipeline/badge.svg)
![Coverage](https://codecov.io/gh/gracobjo/efactura/branch/main/graph/badge.svg)
![Security](https://github.com/gracobjo/efactura/workflows/CI%2FCD%20Pipeline/badge.svg?label=security)
```

### 🚀 **Opciones de Despliegue**

#### **Backend:**
- **Heroku** - Fácil despliegue con Git
- **Railway** - Despliegue automático
- **Render** - Gratuito para proyectos pequeños
- **DigitalOcean** - App Platform
- **AWS/GCP** - Para proyectos empresariales

#### **Frontend:**
- **Vercel** - Optimizado para React
- **Netlify** - Despliegue automático
- **GitHub Pages** - Gratuito
- **Firebase Hosting** - Integración con Google

---

## 🌐 Google Colab

### 🚀 Usar eFactura en Google Colab

Para ejecutar el proyecto directamente en Google Colab sin instalar nada localmente:

1. **Abre Google Colab:** https://colab.research.google.com/
2. **Sube el archivo:** `demo_colab.ipynb` desde este repositorio
3. **Ejecuta las celdas** en orden

**Nota importante:** En Colab, usa `%pip install` en lugar de `!pip install` para evitar advertencias.

### 📋 Pasos en Colab:

```python
# 1. Clonar el repositorio
!git clone https://github.com/gracobjo/efactura.git
%cd efactura

# 2. Instalar dependencias (usando %pip)
%pip install -r requirements.txt

# 3. Inicializar y poblar la base de datos
import os
os.makedirs('instance', exist_ok=True)
!python run.py &
!python poblar_db.py

# 4. Analizar facturas
!python analisis_facturas.py

# 5. Generar PDF de ejemplo
from app import create_app
from app.models.factura import Cliente, Item, Factura
from app.services import pdf_generator

app = create_app()
app.app_context().push()

cliente = Cliente("Demo Colab", "Calle Colab 1", "COLAB123")
items = [Item("Producto Colab", 1, 99.99)]
factura = Factura(cliente, items)
pdf_path = pdf_generator.generar_pdf(factura, "colab_demo")
print("PDF generado en:", pdf_path)
```

### ✅ Ventajas de usar Colab:
- **Sin instalación local** de Python o dependencias
- **Acceso gratuito** a recursos de computación
- **Interfaz web** fácil de usar
- **Compartir notebooks** fácilmente

---

## 🐙 Comandos Git Utilizados

### 📋 Resumen de Comandos Git en el Proyecto

Durante el desarrollo de eFactura, hemos utilizado los siguientes comandos de Git para gestionar el versionado del código:

#### 🔧 **Configuración Inicial**
```bash
# Inicializar repositorio Git (ya existía)
git init

# Verificar estado del repositorio
git status

# Verificar ramas locales y remotas
git branch -a
```

#### 📤 **Gestión de Cambios**
```bash
# Agregar todos los archivos al staging area
git add .

# Agregar archivo específico
git add README.md

# Ver archivos en staging area
git status

# Crear commit con mensaje descriptivo
git commit -m "feat: Complete eFactura project with API endpoints, tests, and documentation"

# Crear commit para documentación
git commit -m "docs: Clarify port usage and add troubleshooting section"

# Crear commit para correcciones
git commit -m "fix: Correct pip install syntax for Colab and add Colab documentation"
```

#### 🔄 **Gestión de Ramas**
```bash
# Ver todas las ramas (locales y remotas)
git branch -a

# Cambiar a rama main
git checkout main

# Crear nueva rama desde rama remota
git fetch origin
git checkout main

# Eliminar rama local master
git branch -d master

# Eliminar rama remota master
git push origin --delete master
```

#### 📡 **Sincronización con GitHub**
```bash
# Verificar repositorios remotos configurados
git remote -v

# Obtener cambios del repositorio remoto
git fetch origin

# Subir cambios a GitHub (rama master)
git push origin master

# Subir cambios a GitHub (rama main)
git push origin main

# Subir cambios forzados (cuando hay conflictos)
git push origin main --force
```

#### 🔍 **Información y Logs**
```bash
# Ver historial de commits (últimos 5)
git log --oneline -5

# Ver diferencias entre ramas
git ls-remote --heads origin
```

### 🎯 **¿Por qué usamos estos comandos?**

#### **1. `git init`**
- **Propósito:** Inicializar un repositorio Git local
- **Cuándo:** Al comenzar un proyecto nuevo
- **Resultado:** Crea la carpeta `.git` con toda la configuración

#### **2. `git add .`**
- **Propósito:** Agregar todos los archivos modificados al staging area
- **Cuándo:** Después de hacer cambios en el código
- **Alternativa:** `git add archivo_especifico` para archivos individuales

#### **3. `git commit -m "mensaje"`**
- **Propósito:** Crear un punto de guardado con los cambios
- **Convención:** Usamos mensajes descriptivos con prefijos:
  - `feat:` para nuevas funcionalidades
  - `docs:` para documentación
  - `fix:` para correcciones
  - `refactor:` para refactorización

#### **4. `git push origin main`**
- **Propósito:** Subir cambios locales al repositorio remoto en GitHub
- **Cuándo:** Después de hacer commits locales
- **Importante:** `origin` es el alias del repositorio remoto

#### **5. `git branch -a`**
- **Propósito:** Ver todas las ramas (locales y remotas)
- **Cuándo:** Para entender la estructura del repositorio
- **Resultado:** Muestra `* main` (rama actual) y `remotes/origin/main`

#### **6. `git checkout main`**
- **Propósito:** Cambiar a la rama main
- **Cuándo:** Para trabajar en la rama principal
- **Nota:** GitHub ahora usa `main` por defecto en lugar de `master`

#### **7. `git push origin main --force`**
- **Propósito:** Forzar la subida de cambios (sobrescribe el historial remoto)
- **Cuándo:** Solo cuando es necesario resolver conflictos
- **⚠️ Precaución:** Puede perder cambios en el repositorio remoto

#### **8. `git push origin --delete master`**
- **Propósito:** Eliminar la rama master del repositorio remoto
- **Cuándo:** Para limpiar y usar solo la rama main
- **Resultado:** Simplifica la estructura del repositorio

### 📚 **Flujo de Trabajo Típico**

```bash
# 1. Hacer cambios en el código
# 2. Verificar qué archivos cambiaron
git status

# 3. Agregar cambios al staging
git add .

# 4. Crear commit con mensaje descriptivo
git commit -m "tipo: descripción del cambio"

# 5. Subir cambios a GitHub
git push origin main

# 6. Verificar que se subieron correctamente
git status
```

### 🔄 **Resolución de Problemas Comunes**

#### **Problema: "Cannot connect to GitHub"**
```bash
# Verificar configuración remota
git remote -v

# Si no hay origin, agregarlo
git remote add origin https://github.com/usuario/repositorio.git
```

#### **Problema: "Branch diverged"**
```bash
# Obtener cambios remotos
git fetch origin

# Hacer merge o rebase
git merge origin/main
# O
git rebase origin/main
```

#### **Problema: "Permission denied"**
```bash
# Configurar credenciales
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

### 🎓 **Buenas Prácticas de Git**

1. **Commits frecuentes:** Hacer commits pequeños y frecuentes
2. **Mensajes descriptivos:** Usar mensajes que expliquen el "qué" y "por qué"
3. **Rama principal limpia:** Mantener `main` siempre funcional
4. **Pull antes de push:** Siempre sincronizar antes de subir cambios
5. **Revisar antes de commit:** Usar `git status` y `git diff` antes de commit

---

## ❓ Preguntas Frecuentes (FAQ)

### ¿Se borran los datos de la base de datos SQLite al cerrar la aplicación?
No. Los datos se guardan de forma persistente en el archivo `instance/eFactura.db`. Solo se pierden si borras manualmente ese archivo.

### ¿Cómo puedo ver o editar la base de datos?
Puedes usar herramientas como **DB Browser for SQLite** o **SQLiteStudio** y abrir el archivo `instance/eFactura.db`.

### ¿Qué datos contiene el QR de la factura?
El QR contiene un JSON con:
- NIF del emisor
- Número de factura
- Fecha
- Total con IVA
- Hash único de la factura
- URL de verificación

### ¿Cómo puedo crear una factura desde PowerShell?
Usa:
```powershell
Invoke-WebRequest -Uri http://localhost:5000/factura `
  -Method POST `
  -ContentType "application/json" `
  -InFile "factura.json" `
  -OutFile "factura.pdf"
```

### ¿Cómo puedo crear una factura desde Linux/Mac (Bash)?
Usa:
```bash
curl -X POST http://localhost:5000/factura -H "Content-Type: application/json" -d @factura.json --output factura.pdf
```

### ¿Cómo puedo probar la API visualmente?
- Abre el archivo `swagger.yaml` en [Swagger Editor](https://editor.swagger.io/)
- Prueba los endpoints y consulta la documentación interactiva

### ¿Qué hago si el QR me dice "Factura no encontrada"?
- Asegúrate de que la factura existe en la base de datos
- Comprueba el ID en la URL del QR y que no hayas borrado la base de datos
- Puedes consultar los IDs existentes con:
  ```bash
  curl http://localhost:5000/facturas
  ```

### ¿Puedo personalizar el diseño del PDF o el contenido del QR?
¡Sí! Modifica `app/services/pdf_generator.py` para cambiar el diseño, los campos del QR o la leyenda.

### ¿Cómo ejecuto los tests automáticos?
Desde la raíz del proyecto:
```bash
pytest
```

### ¿Cómo puedo hacer un backup de la base de datos?
Copia el archivo `instance/eFactura.db` a otro lugar:
```bash
cp instance/eFactura.db backup_efactura.db
```

### ¿Puedo desplegar esto en la nube?
Sí. Puedes desplegar el backend en Heroku, Render, Railway, etc. y el frontend en Vercel, Netlify, etc. Recuerda configurar CORS si frontend y backend están en dominios distintos.

--- 