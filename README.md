# eFactura

Sistema de facturación electrónica completo con backend en Python (Flask) y frontend en React.

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

### Crear una Factura

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

### Verificar una Factura

1. Haz clic en la pestaña **"Verificar Factura"**
2. Ingresa el ID de la factura
3. Haz clic en **"Verificar"**
4. Se mostrarán los datos básicos de la factura

### Análisis de Facturación

```bash
python analisis_facturas.py
```
Esto mostrará:
- Total facturado por mes
- Facturación por cliente
- Gráfico de barras

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

## 🚀 Despliegue

### Opciones de Despliegue

**Backend:**
- Heroku
- Railway
- Render
- DigitalOcean
- AWS/GCP

**Frontend:**
- Vercel
- Netlify
- GitHub Pages
- Firebase Hosting

### Variables de Entorno

**Backend:**
```bash
FLASK_ENV=production
DATABASE_URL=sqlite:///efactura.db
SECRET_KEY=tu-clave-secreta
```

**Frontend:**
```bash
REACT_APP_API_URL=https://tu-api.herokuapp.com
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