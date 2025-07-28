#!/usr/bin/env python3
"""
Ejemplo de Aplicación Externa
Demuestra cómo una aplicación externa puede usar el API de eFactura
sin guardar datos en la base de datos del sistema
"""

import requests
import json
from datetime import datetime

class AplicacionExterna:
    def __init__(self, api_base_url="http://localhost:5000"):
        self.api_base_url = api_base_url
        self.headers = {
            'Content-Type': 'application/json'
        }
    
    def validar_factura(self, factura_data):
        """Valida una factura antes de procesarla"""
        try:
            response = requests.post(
                f"{self.api_base_url}/api/validar-factura",
                headers=self.headers,
                json=factura_data
            )
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500
    
    def procesar_factura(self, factura_data):
        """Procesa una factura sin guardarla en la BD de eFactura"""
        try:
            response = requests.post(
                f"{self.api_base_url}/api/procesar-factura",
                headers=self.headers,
                json=factura_data
            )
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500
    
    def calcular_total(self, items):
        """Calcula el total de una lista de items"""
        try:
            response = requests.post(
                f"{self.api_base_url}/api/calcular-total",
                headers=self.headers,
                json={"items": items}
            )
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500

def ejemplo_migracion_facturas():
    """Ejemplo: Migrar facturas desde un sistema externo"""
    print("🔄 Ejemplo: Migración de Facturas desde Sistema Externo")
    print("=" * 60)
    
    # Simular facturas de un sistema externo (ej: Contasimple, Sage, etc.)
    facturas_externas = [
        {
            "cliente": {
                "nombre": "Empresa Contasimple S.L.",
                "direccion": "Calle Contasimple 123, 28001 Madrid",
                "identificacion": "B87654321"
            },
            "items": [
                {
                    "descripcion": "Servicio de Contabilidad",
                    "cantidad": 12,
                    "precio": 150.00
                },
                {
                    "descripcion": "Asesoría Fiscal",
                    "cantidad": 1,
                    "precio": 500.00
                }
            ]
        },
        {
            "cliente": {
                "nombre": "Cliente Sage",
                "direccion": "Av. Sage 456, 08001 Barcelona",
                "identificacion": "A12345678"
            },
            "items": [
                {
                    "descripcion": "Software de Gestión",
                    "cantidad": 1,
                    "precio": 2500.00
                }
            ]
        }
    ]
    
    app_externa = AplicacionExterna()
    
    for i, factura in enumerate(facturas_externas, 1):
        print(f"\n📄 Procesando Factura {i}...")
        
        # 1. Validar la factura
        print("   ✅ Validando factura...")
        validacion, status = app_externa.validar_factura(factura)
        
        if status == 200:
            print("   ✅ Factura válida")
            
            # 2. Procesar la factura
            print("   🔄 Procesando factura...")
            resultado, status = app_externa.procesar_factura(factura)
            
            if status == 200:
                print(f"   ✅ Factura procesada exitosamente")
                print(f"   📊 Número: {resultado['numero']}")
                print(f"   💰 Total: €{resultado['total']:.2f}")
                print(f"   📅 Fecha: {resultado['fecha']}")
                
                # Aquí la aplicación externa podría:
                # - Guardar en su propia BD
                # - Generar PDF
                # - Enviar por email
                # - etc.
                
            else:
                print(f"   ❌ Error al procesar: {resultado}")
        else:
            print(f"   ❌ Factura inválida: {validacion}")

def ejemplo_calculo_totales():
    """Ejemplo: Calcular totales para presupuestos"""
    print("\n🧮 Ejemplo: Cálculo de Totales para Presupuestos")
    print("=" * 60)
    
    # Simular items de un presupuesto
    items_presupuesto = [
        {"descripcion": "Diseño Web", "cantidad": 1, "precio": 1500.00},
        {"descripcion": "Desarrollo Frontend", "cantidad": 20, "precio": 75.00},
        {"descripcion": "Desarrollo Backend", "cantidad": 15, "precio": 100.00},
        {"descripcion": "Testing", "cantidad": 8, "precio": 50.00}
    ]
    
    app_externa = AplicacionExterna()
    
    print("📋 Calculando total del presupuesto...")
    resultado, status = app_externa.calcular_total(items_presupuesto)
    
    if status == 200:
        print("✅ Total calculado exitosamente")
        print(f"💰 Total: €{resultado['total']:.2f}")
        print(f"📊 Cantidad de items: {resultado['cantidad_items']}")
        
        print("\n📋 Desglose:")
        for item in resultado['subtotales']:
            print(f"   • {item['descripcion']}: {item['cantidad']} x €{item['precio']:.2f} = €{item['subtotal']:.2f}")
    else:
        print(f"❌ Error al calcular: {resultado}")

def ejemplo_validacion_lote():
    """Ejemplo: Validar un lote de facturas"""
    print("\n✅ Ejemplo: Validación de Lote de Facturas")
    print("=" * 60)
    
    # Simular lote de facturas con errores
    lote_facturas = [
        {
            "cliente": {"nombre": "Cliente Válido", "direccion": "Test", "identificacion": "B12345678"},
            "items": [{"descripcion": "Test", "cantidad": 1, "precio": 100}]
        },
        {
            "cliente": {"nombre": "Cliente Inválido", "direccion": "Test", "identificacion": "INVALID"},
            "items": [{"descripcion": "Test", "cantidad": 1, "precio": 100}]
        },
        {
            "cliente": {"nombre": "Cliente Válido 2", "direccion": "Test", "identificacion": "A87654321"},
            "items": [{"descripcion": "Test", "cantidad": 1, "precio": 100}]
        }
    ]
    
    app_externa = AplicacionExterna()
    
    print("🔍 Validando lote de facturas...")
    
    for i, factura in enumerate(lote_facturas, 1):
        resultado, status = app_externa.validar_factura(factura)
        
        if status == 200:
            print(f"   ✅ Factura {i}: Válida")
        else:
            print(f"   ❌ Factura {i}: Inválida - {resultado.get('errores', ['Error desconocido'])}")

if __name__ == "__main__":
    print("🚀 Ejemplo de Aplicación Externa usando eFactura API")
    print("=" * 60)
    print("Este ejemplo muestra cómo una aplicación externa puede:")
    print("• Validar facturas sin guardarlas")
    print("• Procesar facturas temporalmente")
    print("• Calcular totales para presupuestos")
    print("• Migrar datos desde otros sistemas")
    print("=" * 60)
    
    try:
        # Ejecutar ejemplos
        ejemplo_migracion_facturas()
        ejemplo_calculo_totales()
        ejemplo_validacion_lote()
        
        print("\n🎉 Todos los ejemplos completados exitosamente!")
        print("💡 Las aplicaciones externas pueden usar estos endpoints")
        print("   sin afectar la base de datos de eFactura")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Asegúrate de que el servidor esté ejecutándose en http://localhost:5000") 