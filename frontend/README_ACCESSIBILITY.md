# 🎯 Documentación de Accesibilidad Web - eFactura

## 📋 Índice

1. [Descripción General](#descripción-general)
2. [Funcionalidades Implementadas](#funcionalidades-implementadas)
3. [Cómo Ejecutar los Tests](#cómo-ejecutar-los-tests)
4. [Configuración del Entorno](#configuración-del-entorno)
5. [Interpretación de Resultados](#interpretación-de-resultados)
6. [Solución de Problemas](#solución-de-problemas)
7. [Integración CI/CD](#integración-cicd)

---

## 🎯 Descripción General

Este sistema implementa **pruebas automatizadas de accesibilidad web** para el proyecto eFactura, asegurando el cumplimiento de los estándares **WCAG 2.1 AA** (Web Content Accessibility Guidelines).

### 🎯 Objetivos

- ✅ Verificar accesibilidad completa de la aplicación
- ✅ Cumplir estándares internacionales WCAG 2.1 AA
- ✅ Detectar regresiones de accesibilidad automáticamente
- ✅ Garantizar experiencia de usuario inclusiva

### 🛠️ Tecnologías Utilizadas

- **Playwright**: Framework de testing automatizado
- **axe-core**: Motor de análisis de accesibilidad
- **WCAG 2.1 AA**: Estándares de accesibilidad
- **React**: Framework de desarrollo frontend

---

## ♿ Funcionalidades Implementadas

### 1. **Análisis WCAG 2.1 AA**
```javascript
// Análisis automático con axe-core
const accessibilityScanResults = await new AxeBuilder({ page })
  .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
  .analyze();
```

**Verificaciones:**
- ✅ Contraste de colores
- ✅ Estructura semántica
- ✅ Atributos ARIA
- ✅ Navegación por teclado
- ✅ Lectores de pantalla

### 2. **Navegación por Teclado**
```jsx
// Tabs enfocables con tabindex
<button 
  role="tab"
  tabIndex={0}
  aria-selected={activeTab === 'crear'}
  aria-controls="panel-crear"
  id="tab-crear"
>
```

**Funcionalidades:**
- ✅ Navegación con Tab
- ✅ Navegación con flechas (← →)
- ✅ Navegación con Home/End
- ✅ Foco visible y gestionado

### 3. **Formularios Accesibles**
```jsx
// Labels asociados y aria-describedby
<label htmlFor="cliente-nombre">
  Nombre completo: <span className="required" aria-label="campo obligatorio">*</span>
</label>
<input 
  id="cliente-nombre"
  aria-describedby="help-nombre"
  required
/>
```

**Características:**
- ✅ Labels asociados con `for` e `id`
- ✅ `aria-describedby` en todos los inputs
- ✅ Indicadores visuales de campos requeridos
- ✅ Estructura semántica con `fieldset` y `legend`

### 4. **Responsive Design Accesible**
```javascript
// Verificación en viewport móvil
await page.setViewportSize({ width: 375, height: 667 });
```

**Verificaciones:**
- ✅ Áreas táctiles de 44x44px mínimo
- ✅ Accesibilidad en dispositivos móviles
- ✅ Análisis específico para viewport móvil

---

## 🚀 Cómo Ejecutar los Tests

### 📋 Prerrequisitos

1. **Node.js** (versión 16 o superior)
2. **npm** o **yarn**
3. **Playwright** instalado

### 🔧 Configuración Inicial

```bash
# 1. Navegar al directorio frontend
cd frontend

# 2. Instalar dependencias
npm install

# 3. Instalar Playwright (si no está instalado)
npx playwright install
```

### 🎯 Comandos de Ejecución

#### **Ejecutar Todos los Tests de Accesibilidad**
```bash
npm run test:accessibility
```

**Resultado esperado:**
```
Running 16 tests using 2 workers
📊 Resultados de accesibilidad:
- ✅ Pases: 21
- ❌ Violaciones: 0
- ⚠️ Incompletos: 3
- 🔍 Inaplicables: 40
16 passed (39.2s)
```

#### **Ver Reporte HTML Detallado**
```bash
npx playwright show-report
```

**Acceso:** http://localhost:9323

#### **Ejecutar Tests con UI Interactiva**
```bash
npx playwright test --ui
```

#### **Ejecutar Tests en Modo Debug**
```bash
npx playwright test --debug
```

#### **Ejecutar Tests Específicos**
```bash
# Solo tests de navegación por teclado
npx playwright test -g "Navegación por teclado"

# Solo tests de formularios
npx playwright test -g "Formulario"
```

### 📊 Comandos Adicionales

```bash
# Ver todos los scripts disponibles
npm run

# Ejecutar tests con video
npx playwright test --video=on

# Ejecutar tests con screenshots
npx playwright test --screenshot=on

# Ejecutar tests en navegadores específicos
npx playwright test --project=chromium
npx playwright test --project="Mobile Chrome"
```

---

## ⚙️ Configuración del Entorno

### 📁 Estructura de Archivos

```
frontend/
├── tests/
│   └── accessibility.spec.js    # Tests de accesibilidad
├── src/
│   ├── App.js                   # Componente principal
│   ├── components/
│   │   └── FacturaForm.js       # Formulario accesible
│   └── App.css                  # Estilos accesibles
├── package.json                 # Dependencias y scripts
├── playwright.config.js         # Configuración de Playwright
└── ACCESSIBILITY_REPORT.md      # Reporte de accesibilidad
```

### 🔧 Configuración de Playwright

```javascript
// playwright.config.js
module.exports = {
  testDir: './tests',
  timeout: 30000,
  expect: {
    timeout: 5000
  },
  use: {
    headless: true,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
    video: 'off',
    screenshot: 'only-on-failure'
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] }
    }
  ]
};
```

---

## 📈 Interpretación de Resultados

### 🎯 Métricas de Éxito

| Métrica | Valor Óptimo | Descripción |
|---------|--------------|-------------|
| **Tests Pasando** | 16/16 | Todos los tests deben pasar |
| **Pases axe-core** | 21+ | Análisis de accesibilidad exitoso |
| **Violaciones WCAG** | 0 | Sin violaciones críticas |
| **Tiempo de Ejecución** | <60s | Rendimiento aceptable |

### 📊 Análisis de Resultados

#### **Resultado Exitoso:**
```
📊 Resultados de accesibilidad:
- ✅ Pases: 21
- ❌ Violaciones: 0
- ⚠️ Incompletos: 3
- 🔍 Inaplicables: 40
16 passed (39.2s)
```

#### **Interpretación:**
- **✅ Pases (21)**: Elementos que cumplen estándares de accesibilidad
- **❌ Violaciones (0)**: Problemas críticos de accesibilidad (debe ser 0)
- **⚠️ Incompletos (3)**: Elementos que requieren revisión manual
- **🔍 Inaplicables (40)**: Elementos no relevantes para accesibilidad

### 🚨 Identificación de Problemas

#### **Violaciones Críticas:**
```
❌ Violaciones encontradas:
1. critical: Elements must meet minimum color contrast ratio requirements
   Criterio WCAG: wcag2aa
   Elementos afectados: 2
```

#### **Solución:**
1. Revisar contraste de colores
2. Ajustar colores según WCAG 2.1 AA
3. Re-ejecutar tests

---

## 🔧 Solución de Problemas

### ❌ Error: "Missing script: test:accessibility"

**Causa:** No estás en el directorio correcto.

**Solución:**
```bash
# Navegar al directorio frontend
cd frontend

# Verificar que estás en el directorio correcto
ls package.json

# Ejecutar tests
npm run test:accessibility
```

### ❌ Error: "No report found"

**Causa:** No se han ejecutado tests recientemente.

**Solución:**
```bash
# Ejecutar tests primero
npm run test:accessibility

# Luego ver reporte
npx playwright show-report
```

### ❌ Error: "Test timeout exceeded"

**Causa:** Problemas de rendimiento o overlay de webpack.

**Solución:**
```bash
# Aumentar timeout en playwright.config.js
timeout: 60000,

# O ejecutar con timeout específico
npx playwright test --timeout=60000
```

### ❌ Error: "Overlay intercepts pointer events"

**Causa:** Overlay de webpack interfiriendo con tests.

**Solución:** Los tests ya incluyen eliminación automática del overlay:
```javascript
// Eliminación automática implementada
await page.evaluate(() => {
  const overlay = document.getElementById('webpack-dev-server-client-overlay');
  if (overlay) overlay.remove();
});
```

### 🔄 Reinicio Completo

Si tienes problemas persistentes:

```bash
# 1. Limpiar caché
npm cache clean --force

# 2. Eliminar node_modules
rm -rf node_modules

# 3. Reinstalar dependencias
npm install

# 4. Reinstalar Playwright
npx playwright install

# 5. Ejecutar tests
npm run test:accessibility
```

---

## 🔄 Integración CI/CD

### 📋 GitHub Actions

```yaml
# .github/workflows/accessibility.yml
name: Accessibility Tests

on:
  pull_request:
    branches: [ main ]
  push:
    branches: [ main ]

jobs:
  accessibility:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json
    
    - name: Install dependencies
      run: |
        cd frontend
        npm ci
    
    - name: Install Playwright
      run: |
        cd frontend
        npx playwright install --with-deps
    
    - name: Start development server
      run: |
        cd frontend
        npm start &
        sleep 30
    
    - name: Run accessibility tests
      run: |
        cd frontend
        npm run test:accessibility
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: accessibility-results
        path: frontend/test-results/
```

### 📋 GitLab CI

```yaml
# .gitlab-ci.yml
accessibility:
  stage: test
  image: node:18
  script:
    - cd frontend
    - npm ci
    - npx playwright install --with-deps
    - npm start &
    - sleep 30
    - npm run test:accessibility
  artifacts:
    paths:
      - frontend/test-results/
    when: always
```

### 📋 Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    stages {
        stage('Setup') {
            steps {
                dir('frontend') {
                    sh 'npm ci'
                    sh 'npx playwright install --with-deps'
                }
            }
        }
        
        stage('Accessibility Tests') {
            steps {
                dir('frontend') {
                    sh 'npm start &'
                    sh 'sleep 30'
                    sh 'npm run test:accessibility'
                }
            }
        }
    }
    
    post {
        always {
            dir('frontend') {
                archiveArtifacts artifacts: 'test-results/**/*'
            }
        }
    }
}
```

---

## 📞 Soporte y Contacto

### 🆘 Problemas Comunes

1. **Tests fallando**: Revisar configuración de navegadores
2. **Timeouts**: Aumentar timeout en configuración
3. **Overlay webpack**: Los tests lo manejan automáticamente
4. **Dependencias**: Reinstalar con `npm ci`

### 📧 Contacto

- **Proyecto**: eFactura - Sistema de Facturación Electrónica
- **Estándares**: WCAG 2.1 AA
- **Herramientas**: Playwright + axe-core
- **Estado**: ✅ Completamente funcional

### 📚 Recursos Adicionales

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Playwright Documentation](https://playwright.dev/)
- [axe-core Documentation](https://github.com/dequelabs/axe-core)
- [Accessibility Testing Best Practices](https://www.w3.org/WAI/ER/tools/)

---

*Documentación generada automáticamente - Última actualización: $(date)* 