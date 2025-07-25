# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2025-01-21

### 🆕 Añadido
- **Documentación UML completa**: Generación de diagramas UML esenciales y opcionales
  - Diagrama de Casos de Uso: Interacciones entre usuarios y sistema
  - Diagrama de Clases: Estructura de clases y relaciones
  - Diagrama de Secuencia: Flujo de interacciones (Crear/Verificar Factura)
  - Diagrama de Actividad: Flujo de trabajo del sistema
  - Diagrama de Estado: Estados de una factura
  - Diagrama de Componentes: Arquitectura de componentes
  - Diagrama de Despliegue: Infraestructura y despliegue
- **Documentación técnica mejorada**:
  - `DEVELOPMENT.md`: Guía completa para desarrolladores
  - `API.md`: Documentación detallada de la API con ejemplos
  - README actualizado con sección de diagramas UML
- **Configuración centralizada**: Sistema de configuración modular por entornos
  - `app/config.py`: Configuración centralizada
  - Soporte para Development, Production y Testing
  - Variables de entorno configurables
- **Sistema de excepciones personalizadas**: Manejo de errores mejorado
  - `app/exceptions.py`: Excepciones específicas del dominio
  - `ValidationError`, `PDFProcessingError`, `StorageError`, `FacturaNotFoundError`
- **Utilidades reutilizables**: Funciones auxiliares centralizadas
  - `app/utils/formatters.py`: Formateo de datos (moneda, fechas, etc.)
  - `app/utils/validators.py`: Validación robusta de datos de entrada
- **Script de migración de BD**: Herramienta para actualizar esquemas de base de datos
  - `migrate_db.py`: Backup, migración y verificación de BD
  - Soporte para actualizaciones de esquema seguras

### 🔧 Mejorado
- **Arquitectura del código**: Refactorización completa para mejor mantenibilidad
  - Separación de responsabilidades en capas bien definidas
  - Eliminación de código duplicado
  - Patrones de diseño implementados (Factory, Repository, Strategy)
- **Manejo de errores**: Sistema consistente de manejo de errores
  - Respuestas de error estandarizadas
  - Logging mejorado
  - Rollback automático en transacciones
- **Validación de datos**: Validación robusta y centralizada
  - Validación de formato de identificación
  - Sanitización de texto
  - Validación de archivos PDF
- **Configuración de herramientas**: Configuración centralizada de herramientas de desarrollo
  - `pyproject.toml`: Configuración de Black, Flake8, Pytest, Coverage
  - Línea de 88 caracteres para Black
  - Reglas de Flake8 optimizadas
- **CI/CD Pipeline**: Mejoras en el pipeline de integración continua
  - Creación automática de directorios necesarios
  - Inclusión de nuevos archivos de configuración
  - Mejor manejo de dependencias

### ♻️ Refactorizado
- **Rutas de API**: Refactorización completa de `app/routes/factura_routes.py`
  - Reducción de complejidad ciclomática
  - Separación de lógica de negocio
  - Uso de servicios y utilidades centralizadas
- **Servicios**: Reorganización de servicios para mejor modularidad
  - `app/services/pdf_extractor.py`: Extracción de datos de PDFs
  - `app/services/storage.py`: Mejor manejo de transacciones
  - `app/services/pdf_generator.py`: Uso de configuración centralizada
- **Modelos**: Mejoras en la estructura de modelos de dominio
  - Mejor encapsulación
  - Métodos más claros y específicos
- **Tests**: Actualización de tests para nueva arquitectura
  - Tests adaptados a nueva configuración
  - Mejor cobertura de casos de error
  - Validación de respuestas de error

### 📝 Documentación
- **README.md**: Documentación completamente renovada
  - Sección de diagramas UML
  - Guías de instalación mejoradas
  - Ejemplos de uso actualizados
  - Información de arquitectura detallada
- **Documentación de API**: Documentación completa y detallada
  - Ejemplos de request/response para todos los endpoints
  - Códigos de error documentados
  - Ejemplos de integración en múltiples lenguajes
- **Guía de desarrollo**: Documentación técnica para desarrolladores
  - Configuración de entorno de desarrollo
  - Convenciones de código
  - Herramientas de debugging y testing
  - Flujo de trabajo recomendado

### 🔒 Seguridad
- **Validación de entrada**: Validación más estricta de datos de entrada
  - Sanitización de texto
  - Validación de tipos de archivo
  - Límites de tamaño de archivo
- **Manejo de errores**: No exposición de información sensible en errores
- **Headers de seguridad**: Configuración de headers de seguridad básicos

### ⚡️ Rendimiento
- **Optimización de consultas**: Mejoras en consultas de base de datos
- **Manejo de memoria**: Mejor gestión de recursos en procesamiento de PDFs
- **Caché**: Implementación básica de caché para configuraciones

### 📦 Dependencias
- Actualizadas dependencias de seguridad
- Añadidas dependencias para herramientas de desarrollo
- Optimización de `requirements.txt`

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