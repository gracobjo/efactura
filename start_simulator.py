#!/usr/bin/env python3
"""
Script para iniciar el simulador de aplicación externa
que se conecta a eFactura API
"""

import subprocess
import time
import webbrowser
import os
import sys
from pathlib import Path

def start_backend():
    """Inicia el servidor backend de Flask"""
    print("🚀 Iniciando servidor backend...")
    
    # Cambiar al directorio raíz del proyecto
    os.chdir(Path(__file__).parent)
    
    try:
        # Iniciar el servidor Flask en segundo plano
        backend_process = subprocess.Popen([
            sys.executable, "app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ Backend iniciado en http://localhost:5000")
        return backend_process
        
    except Exception as e:
        print(f"❌ Error al iniciar backend: {e}")
        return None

def open_simulator():
    """Abre el simulador en el navegador"""
    simulator_path = Path(__file__).parent / "frontend" / "public" / "simulator.html"
    
    if simulator_path.exists():
        print("🌐 Abriendo simulador en el navegador...")
        webbrowser.open(f"file://{simulator_path.absolute()}")
        print("✅ Simulador abierto en el navegador")
    else:
        print(f"❌ No se encontró el archivo del simulador: {simulator_path}")

def main():
    """Función principal"""
    print("🎯 Simulador de Aplicación Externa - eFactura")
    print("=" * 50)
    
    # Iniciar backend
    backend_process = start_backend()
    
    if backend_process:
        # Esperar un momento para que el servidor se inicie
        print("⏳ Esperando que el servidor esté listo...")
        time.sleep(3)
        
        # Abrir simulador
        open_simulator()
        
        print("\n📋 Instrucciones:")
        print("1. El simulador se abrirá en tu navegador")
        print("2. Haz clic en 'Probar Conexión API' para verificar la conexión")
        print("3. Usa 'Crear Factura de Prueba' para crear una factura")
        print("4. Usa 'Obtener Facturas' para ver las facturas existentes")
        print("\n🛑 Para detener el servidor, presiona Ctrl+C")
        
        try:
            # Mantener el script ejecutándose
            backend_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo servidor...")
            backend_process.terminate()
            print("✅ Servidor detenido")
    else:
        print("❌ No se pudo iniciar el simulador")

if __name__ == "__main__":
    main() 