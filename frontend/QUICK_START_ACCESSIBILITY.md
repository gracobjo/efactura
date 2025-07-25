# 🚀 Guía Rápida - Tests de Accesibilidad

## ⚡ Ejecución Rápida

### 1️⃣ **Navegar al Directorio Correcto**
```bash
cd frontend
```

### 2️⃣ **Ejecutar Tests de Accesibilidad**
```bash
npm run test:accessibility
```

### 3️⃣ **Ver Reporte HTML**
```bash
npx playwright show-report
```

---

## 📊 Resultado Esperado

```
Running 16 tests using 2 workers
📊 Resultados de accesibilidad:
- ✅ Pases: 21
- ❌ Violaciones: 0
- ⚠️ Incompletos: 3
- 🔍 Inaplicables: 40
16 passed (39.2s)
```

---

## 🎯 Comandos Útiles

| Comando | Descripción |
|---------|-------------|
| `npm run test:accessibility` | Ejecutar todos los tests |
| `npx playwright show-report` | Ver reporte HTML |
| `npx playwright test --ui` | UI interactiva |
| `npx playwright test --debug` | Modo debug |
| `npx playwright test -g "Navegación"` | Tests específicos |

---

## ❌ Solución de Problemas Rápidos

### **Error: "Missing script"**
```bash
# Asegúrate de estar en el directorio correcto
pwd  # Debe mostrar: .../efactura/frontend
npm run test:accessibility
```

### **Error: "No report found"**
```bash
# Ejecuta tests primero
npm run test:accessibility
# Luego ve el reporte
npx playwright show-report
```

### **Error: "Test timeout"**
```bash
# Aumenta timeout
npx playwright test --timeout=60000
```

---

## 📋 Checklist de Verificación

- [ ] Estás en el directorio `frontend`
- [ ] Node.js está instalado (versión 16+)
- [ ] Dependencias instaladas (`npm install`)
- [ ] Playwright instalado (`npx playwright install`)
- [ ] Tests ejecutándose sin errores
- [ ] Reporte HTML accesible

---

## 🎯 Estado del Sistema

**✅ FUNCIONALIDADES VERIFICADAS:**
- ♿ WCAG 2.1 AA compliance
- ⌨️ Navegación por teclado
- 📝 Formularios accesibles
- 📱 Responsive design
- 🎨 Contraste de colores
- 🗣️ Lectores de pantalla

**📈 MÉTRICAS:**
- Tests: 16/16 pasando
- Pases axe-core: 21
- Violaciones: 0
- Tiempo: ~39 segundos

---

## 📞 Soporte

- **Documentación completa**: `README_ACCESSIBILITY.md`
- **Reporte detallado**: `ACCESSIBILITY_REPORT.md`
- **Tests**: `tests/accessibility.spec.js`

---

*Guía rápida - Última actualización: $(date)* 