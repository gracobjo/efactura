# Diagramas UML - Sistema eFactura

Este directorio contiene todos los diagramas UML esenciales para el sistema eFactura, creados en sintaxis PlantUML.

## 📋 Diagramas Disponibles

### Diagramas Esenciales

1. **`01_diagrama_casos_uso.puml`** - Diagrama de Casos de Uso
   - Muestra las interacciones entre usuarios y el sistema
   - Define las funcionalidades principales desde la perspectiva del usuario
   - Incluye actores: Usuario, Administrador, Sistema Externo

2. **`02_diagrama_clases.puml`** - Diagrama de Clases
   - Define la estructura de clases del sistema
   - Muestra atributos, métodos y relaciones entre clases
   - Incluye clases de dominio, servicios, utilidades y excepciones

3. **`03_diagrama_secuencia.puml`** - Diagrama de Secuencia (Crear Factura)
   - Ilustra el flujo de interacción para crear una factura
   - Muestra el intercambio de mensajes entre componentes
   - Incluye validación, almacenamiento y generación de PDF

4. **`04_diagrama_secuencia_verificacion.puml`** - Diagrama de Secuencia (Verificar Factura)
   - Muestra el flujo de verificación de facturas
   - Incluye búsqueda en BD y formateo de datos
   - Manejo de casos de factura no encontrada

5. **`05_diagrama_actividad.puml`** - Diagrama de Actividad
   - Describe el flujo de trabajo del sistema
   - Muestra las decisiones y acciones del sistema
   - Cubre todas las operaciones principales

### Diagramas Opcionales

6. **`06_diagrama_estado.puml`** - Diagrama de Estado
   - Muestra los estados de una factura a lo largo de su ciclo de vida
   - Incluye transiciones entre estados
   - Define el comportamiento complejo de las facturas

7. **`07_diagrama_componentes.puml`** - Diagrama de Componentes
   - Representa la estructura física de componentes
   - Muestra las dependencias entre módulos
   - Incluye frontend, backend, servicios y utilidades

8. **`08_diagrama_despliegue.puml`** - Diagrama de Despliegue
   - Describe la distribución física del hardware y software
   - Muestra la arquitectura de despliegue
   - Incluye desarrollo, producción y CI/CD

## 🛠️ Cómo Usar los Diagramas

### Opción 1: PlantUML Online
1. Ve a [PlantUML Online Server](http://www.plantuml.com/plantuml/uml/)
2. Copia y pega el contenido de cualquier archivo `.puml`
3. El diagrama se generará automáticamente

### Opción 2: Extensiones de VS Code
1. Instala la extensión "PlantUML" en VS Code
2. Abre cualquier archivo `.puml`
3. Usa `Ctrl+Shift+P` y selecciona "PlantUML: Preview Current Diagram"

### Opción 3: PlantUML Local
```bash
# Instalar PlantUML
npm install -g plantuml

# Generar diagrama
plantuml diagrama.puml
```

## 📊 Descripción de los Diagramas

### Diagrama de Casos de Uso
- **Propósito**: Mostrar las funcionalidades del sistema desde la perspectiva del usuario
- **Elementos clave**: Actores, casos de uso, relaciones include/extend
- **Beneficios**: Entender qué puede hacer el usuario con el sistema

### Diagrama de Clases
- **Propósito**: Definir la estructura de clases y sus relaciones
- **Elementos clave**: Clases, atributos, métodos, herencia, asociaciones
- **Beneficios**: Base para el diseño orientado a objetos

### Diagrama de Secuencia
- **Propósito**: Mostrar la interacción entre objetos en el tiempo
- **Elementos clave**: Actores, objetos, mensajes, activación
- **Beneficios**: Entender el flujo de operaciones complejas

### Diagrama de Actividad
- **Propósito**: Describir el flujo de trabajo del sistema
- **Elementos clave**: Actividades, decisiones, flujos
- **Beneficios**: Visualizar procesos de negocio

### Diagrama de Estado
- **Propósito**: Mostrar los estados de un objeto y sus transiciones
- **Elementos clave**: Estados, transiciones, eventos
- **Beneficios**: Entender comportamientos complejos

### Diagrama de Componentes
- **Propósito**: Representar la estructura física de componentes
- **Elementos clave**: Componentes, interfaces, dependencias
- **Beneficios**: Arquitectura del sistema

### Diagrama de Despliegue
- **Propósito**: Mostrar la distribución física del sistema
- **Elementos clave**: Nodos, componentes, conexiones
- **Beneficios**: Planificación de infraestructura

## 🔄 Actualización de Diagramas

Los diagramas están basados en la arquitectura actual del sistema eFactura. Si se realizan cambios significativos en:

- Estructura de clases
- Flujos de trabajo
- Arquitectura de componentes
- Configuración de despliegue

**Recuerda actualizar los diagramas correspondientes** para mantener la documentación sincronizada con el código.

## 📝 Notas Técnicas

- Todos los diagramas usan sintaxis PlantUML estándar
- Los diagramas están optimizados para legibilidad
- Se incluyen notas explicativas donde es necesario
- Los colores y estilos son consistentes entre diagramas

## 🎯 Uso Recomendado

1. **Para desarrolladores nuevos**: Comenzar con el diagrama de casos de uso
2. **Para entender la arquitectura**: Revisar el diagrama de clases y componentes
3. **Para debugging**: Usar los diagramas de secuencia
4. **Para planificación**: Consultar el diagrama de despliegue
5. **Para procesos de negocio**: Analizar el diagrama de actividad

---

*Estos diagramas son parte de la documentación técnica del sistema eFactura y deben mantenerse actualizados con el código.* 