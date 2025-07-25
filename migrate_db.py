#!/usr/bin/env python3
"""
Script para migrar la base de datos existente a la nueva estructura
"""
import os
import shutil
from datetime import datetime
from app import create_app, db
from app.services.storage import FacturaDB, ClienteDB, ItemDB

def backup_database():
    """Crea un backup de la base de datos actual"""
    db_path = os.path.join('instance', 'eFactura.db')
    if os.path.exists(db_path):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f'instance/eFactura_backup_{timestamp}.db'
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup creado: {backup_path}")
        return backup_path
    return None

def migrate_database():
    """Migra la base de datos a la nueva estructura"""
    print("🔄 Iniciando migración de la base de datos...")
    
    # Crear backup
    backup_path = backup_database()
    
    try:
        # Crear nueva aplicación con configuración de desarrollo
        app = create_app('development')
        
        with app.app_context():
            # Eliminar tablas existentes si existen
            db.drop_all()
            print("🗑️  Tablas existentes eliminadas")
            
            # Crear nuevas tablas
            db.create_all()
            print("✅ Nuevas tablas creadas")
            
            # Verificar que las tablas se crearon correctamente
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 Tablas creadas: {', '.join(tables)}")
            
            print("✅ Migración completada exitosamente")
            
            if backup_path:
                print(f"💾 Backup disponible en: {backup_path}")
                
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        if backup_path:
            print(f"🔄 Puedes restaurar el backup desde: {backup_path}")
        return False
    
    return True

def verify_migration():
    """Verifica que la migración fue exitosa"""
    print("🔍 Verificando migración...")
    
    try:
        app = create_app('development')
        
        with app.app_context():
            # Verificar que las tablas existen
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            expected_tables = ['clientes', 'facturas', 'items']
            missing_tables = [table for table in expected_tables if table not in tables]
            
            if missing_tables:
                print(f"❌ Tablas faltantes: {missing_tables}")
                return False
            
            print("✅ Todas las tablas están presentes")
            
            # Verificar estructura de las tablas
            for table_name in expected_tables:
                columns = [col['name'] for col in inspector.get_columns(table_name)]
                print(f"📋 {table_name}: {', '.join(columns)}")
            
            print("✅ Verificación completada exitosamente")
            return True
            
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Script de migración de base de datos")
    print("=" * 50)
    
    # Preguntar confirmación
    response = input("¿Deseas continuar con la migración? (y/N): ")
    if response.lower() != 'y':
        print("❌ Migración cancelada")
        exit(0)
    
    # Ejecutar migración
    if migrate_database():
        # Verificar migración
        if verify_migration():
            print("\n🎉 Migración completada exitosamente!")
            print("La aplicación está lista para usar.")
        else:
            print("\n⚠️  La migración se completó pero hay problemas de verificación.")
    else:
        print("\n❌ La migración falló.")
        print("Revisa los errores anteriores.") 