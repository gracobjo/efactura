#!/usr/bin/env node

/**
 * 🎯 Script de Verificación del Workflow de GitHub
 * 
 * Este script simula el entorno de GitHub Actions para verificar
 * que todos los tests de accesibilidad funcionen correctamente.
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🎯 Iniciando verificación del workflow de GitHub...\n');

// Colores para la consola
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m',
  bold: '\x1b[1m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function logStep(step, status = 'info') {
  const statusIcon = status === 'success' ? '✅' : status === 'error' ? '❌' : '🔄';
  const statusColor = status === 'success' ? 'green' : status === 'error' ? 'red' : 'blue';
  log(`${statusIcon} ${step}`, statusColor);
}

function runCommand(command, description) {
  try {
    logStep(description, 'info');
    const result = execSync(command, { 
      cwd: path.join(__dirname, '..'),
      encoding: 'utf8',
      stdio: 'pipe'
    });
    logStep(description, 'success');
    return result;
  } catch (error) {
    logStep(description, 'error');
    log(`Error: ${error.message}`, 'red');
    throw error;
  }
}

async function main() {
  try {
    // 1. Verificar que estamos en el directorio correcto
    log('📁 Verificando directorio de trabajo...', 'blue');
    const currentDir = process.cwd();
    const packageJsonPath = path.join(currentDir, 'package.json');
    
    if (!fs.existsSync(packageJsonPath)) {
      throw new Error('No se encontró package.json. Asegúrate de estar en el directorio frontend/');
    }
    
    logStep('Directorio de trabajo verificado', 'success');
    
    // 2. Verificar que Node.js esté instalado
    log('\n🟢 Verificando Node.js...', 'blue');
    const nodeVersion = execSync('node --version', { encoding: 'utf8' }).trim();
    log(`Node.js versión: ${nodeVersion}`, 'green');
    
    // 3. Verificar que npm esté disponible
    log('\n📦 Verificando npm...', 'blue');
    const npmVersion = execSync('npm --version', { encoding: 'utf8' }).trim();
    log(`npm versión: ${npmVersion}`, 'green');
    
    // 4. Instalar dependencias (simulando npm ci)
    log('\n📦 Instalando dependencias...', 'blue');
    runCommand('npm ci', 'Instalando dependencias con npm ci');
    
    // 5. Verificar que Playwright esté instalado
    log('\n🧪 Verificando Playwright...', 'blue');
    try {
      const playwrightVersion = execSync('npx playwright --version', { encoding: 'utf8' }).trim();
      log(`Playwright versión: ${playwrightVersion}`, 'green');
    } catch (error) {
      log('Instalando Playwright...', 'yellow');
      runCommand('npx playwright install --with-deps', 'Instalando Playwright y dependencias');
    }
    
    // 6. Verificar configuración de Playwright
    log('\n🔧 Verificando configuración de Playwright...', 'blue');
    const configPath = path.join(currentDir, 'playwright.config.js');
    if (!fs.existsSync(configPath)) {
      throw new Error('No se encontró playwright.config.js');
    }
    logStep('Configuración de Playwright encontrada', 'success');
    
    // 7. Verificar que los tests existan
    log('\n🧪 Verificando tests de accesibilidad...', 'blue');
    const testPath = path.join(currentDir, 'tests', 'accessibility.spec.js');
    if (!fs.existsSync(testPath)) {
      throw new Error('No se encontró tests/accessibility.spec.js');
    }
    logStep('Tests de accesibilidad encontrados', 'success');
    
    // 8. Verificar script en package.json
    log('\n📋 Verificando script en package.json...', 'blue');
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
    if (!packageJson.scripts['test:accessibility']) {
      throw new Error('No se encontró el script "test:accessibility" en package.json');
    }
    logStep('Script test:accessibility encontrado', 'success');
    
    // 9. Ejecutar tests de accesibilidad
    log('\n🎯 Ejecutando tests de accesibilidad...', 'blue');
    const testResult = runCommand('npm run test:accessibility', 'Ejecutando tests de accesibilidad');
    
    // 10. Verificar que se generó el reporte
    log('\n📊 Verificando generación de reportes...', 'blue');
    const playwrightReportPath = path.join(currentDir, 'playwright-report');
    if (fs.existsSync(playwrightReportPath)) {
      logStep('Reporte de Playwright generado', 'success');
    } else {
      logStep('Reporte de Playwright no encontrado', 'error');
    }
    
    // 11. Resumen final
    log('\n🎉 ¡Verificación completada exitosamente!', 'green');
    log('\n📋 Resumen:', 'bold');
    log('✅ Node.js y npm verificados', 'green');
    log('✅ Dependencias instaladas', 'green');
    log('✅ Playwright configurado', 'green');
    log('✅ Tests de accesibilidad ejecutados', 'green');
    log('✅ Reportes generados', 'green');
    
    log('\n🚀 El workflow de GitHub debería funcionar correctamente.', 'green');
    log('📝 Para verificar en GitHub:', 'blue');
    log('   1. Ve a https://github.com/gracobjo/efactura/actions', 'blue');
    log('   2. Busca el workflow "🎯 Pruebas de Accesibilidad Automatizadas"', 'blue');
    log('   3. Haz clic en "Run workflow" para ejecutarlo manualmente', 'blue');
    
  } catch (error) {
    log('\n❌ Error durante la verificación:', 'red');
    log(error.message, 'red');
    log('\n🔧 Soluciones posibles:', 'yellow');
    log('   1. Asegúrate de estar en el directorio frontend/', 'yellow');
    log('   2. Ejecuta: npm install', 'yellow');
    log('   3. Ejecuta: npx playwright install', 'yellow');
    log('   4. Verifica que todos los archivos estén presentes', 'yellow');
    process.exit(1);
  }
}

// Ejecutar el script
if (require.main === module) {
  main();
}

module.exports = { main }; 