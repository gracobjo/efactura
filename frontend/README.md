# eFactura Frontend

Frontend en React para el sistema de facturación electrónica eFactura.

## Características

- **Crear Facturas**: Formulario dinámico para crear facturas con datos de cliente e ítems
- **Verificar Facturas**: Consulta de facturas por ID
- **Descarga automática de PDF**: Al crear una factura, se descarga automáticamente el PDF generado
- **Diseño responsive**: Interfaz moderna y adaptable a diferentes dispositivos
- **Integración con API REST**: Conecta con el backend Flask

## Instalación

1. **Instalar dependencias:**
   ```bash
   cd frontend
   npm install
   ```

2. **Configurar la API:**
   - Por defecto, el frontend se conecta a `http://localcdhost:5000`
   - Para cambiar la URL de la API, crea un archivo `.env` en la carpeta `frontend`:
     ```
     REACT_APP_API_URL=http://tu-api-url.com
     ```

## Uso

1. **Iniciar el servidor de desarrollo:**
   ```bash
   npm start
   ```
   El frontend estará disponible en `http://localhost:3000`

2. **Asegúrate de que el backend Flask esté ejecutándose:**
   ```bash
   # En otra terminal, desde la raíz del proyecto
   python run.py
   ```

## Estructura del Proyecto

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── FacturaForm.js      # Formulario para crear facturas
│   │   └── FacturaVerificar.js # Consulta de facturas
│   ├── App.js                  # Componente principal
│   ├── App.css                 # Estilos
│   ├── api.js                  # Configuración de la API
│   └── index.js
├── package.json
└── README.md
```

## Funcionalidades

### Crear Factura
- Formulario con datos del cliente (nombre, dirección, identificación)
- Ítems dinámicos (agregar/eliminar productos/servicios)
- Validación de campos requeridos
- Descarga automática del PDF generado

### Verificar Factura
- Consulta por ID de factura
- Visualización de datos básicos (número, fecha, cliente, total)
- Manejo de errores si la factura no existe

## Tecnologías Utilizadas

- **React 18**: Framework de JavaScript
- **Axios**: Cliente HTTP para llamadas a la API
- **CSS3**: Estilos modernos y responsive
- **HTML5**: Estructura semántica

## Desarrollo

### Scripts Disponibles

- `npm start`: Inicia el servidor de desarrollo
- `npm build`: Construye la aplicación para producción
- `npm test`: Ejecuta las pruebas
- `npm eject`: Expone la configuración de webpack (irreversible)

### Personalización

- **Estilos**: Modifica `src/App.css` para cambiar la apariencia
- **API**: Ajusta `src/api.js` para modificar las llamadas al backend
- **Componentes**: Extiende los componentes en `src/components/`

## Despliegue

Para desplegar en producción:

1. **Construir la aplicación:**
   ```bash
   npm run build
   ```

2. **Los archivos generados estarán en la carpeta `build/`**

3. **Subir a tu servidor web o plataforma de hosting**

## Notas

- El frontend requiere que el backend Flask esté ejecutándose
- Los PDFs se descargan automáticamente al crear una factura
- La aplicación es completamente responsive y funciona en móviles 