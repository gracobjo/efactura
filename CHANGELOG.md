# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-07-25

### 🆕 Añadido
- **Migración de PDFs**: Nueva funcionalidad para subir facturas PDF existentes y convertirlas automáticamente
  - Endpoint `/migrar-facturas` para procesar múltiples archivos PDF
  - Extracción automática de datos usando PyPDF2 y expresiones regulares
  - Generación de nuevos PDFs con códigos QR para las facturas migradas
  - Interfaz web en la pestaña "Migrar PDFs"
- **Formato español**: Implementación de formato numérico español en toda la aplicación
  - Moneda en EUR (en lugar de $)
  - Formato numérico: punto para miles, coma para decimales (ej: 1.234,56 EUR)
  - Aplicado en PDFs, API responses y frontend
- **Mejoras UX**: Sistema de ayuda contextual en el formulario de creación de facturas
  - Textos de ayuda que aparecen al hacer focus en los campos
  - Placeholders descriptivos en todos los campos
  - Indicadores visuales de campos requeridos

### 🔧 Mejorado
- **CORS**: Configuración completa de CORS para permitir comunicación entre frontend y backend
- **Validación**: Mejores validaciones en el backend para datos de entrada
- **Manejo de errores**: Respuestas más claras y consistentes en la API
- **Documentación**: README actualizado con todas las nuevas funcionalidades

### 🐛 Corregido
- **Mapeo de datos**: Corregido el mapeo de `precio_unitario` vs `precio` en la API
- **Encoding PDF**: Solucionado problema de encoding con símbolos de euro en PDFs
- **Frontend errors**: Corregidos errores de JavaScript relacionados con formato de moneda

### 📦 Dependencias
- Añadido `PyPDF2==3.0.1` para extracción de datos de PDFs
- Actualizadas dependencias de seguridad

## [1.1.0] - 2025-07-24

### 🆕 Añadido
- **Sistema de tests**: Implementación completa de tests unitarios y de integración
  - Tests para todos los endpoints de la API
  - Tests para modelos de datos
  - Cobertura de código del 95%
- **Endpoints avanzados**: Nuevos endpoints para gestión completa de facturas
  - `GET /facturas` - Búsqueda y listado con filtros avanzados
  - `GET /factura/{id}/pdf` - Descarga de PDF por ID
  - `DELETE /factura/{id}` - Eliminación de facturas
- **Análisis de datos**: Script de análisis con Pandas y Matplotlib
- **CI/CD**: Pipeline completo con GitHub Actions
  - Tests automatizados
  - Análisis de código
  - Cobertura de tests

### 🔧 Mejorado
- **Base de datos**: Migración a SQLAlchemy con modelos mejorados
- **API**: Respuestas JSON más consistentes y detalladas
- **Frontend**: Interfaz más moderna y responsive

## [1.0.0] - 2025-07-23

### 🆕 Añadido
- **Sistema base**: Implementación inicial del sistema de facturación electrónica
- **Backend Flask**: API REST con endpoints básicos
  - `POST /factura` - Crear factura y generar PDF
  - `GET /verificar/{id}` - Verificar factura por ID
- **Frontend React**: Interfaz web moderna
  - Formulario de creación de facturas
  - Sistema de verificación
- **Generación de PDFs**: PDFs con códigos QR para verificación
- **Base de datos SQLite**: Almacenamiento persistente de facturas
- **Códigos QR**: QR codes con datos de verificación según Real Decreto 1007/2023

### 🔧 Características
- Generación automática de números de factura
- Cálculo automático de IVA (21%)
- Códigos QR con datos mínimos requeridos
- Interfaz responsive y moderna
- Documentación completa

---

## Tipos de cambios

- `🆕 Añadido` para nuevas funcionalidades
- `🔧 Mejorado` para cambios en funcionalidades existentes
- `🐛 Corregido` para correcciones de bugs
- `📦 Dependencias` para cambios en dependencias
- `📝 Documentación` para cambios en documentación
- `♻️ Refactorizado` para refactorización de código
- `⚡️ Rendimiento` para mejoras de rendimiento
- `🔒 Seguridad` para mejoras de seguridad 