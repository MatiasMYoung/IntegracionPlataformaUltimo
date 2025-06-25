#!/usr/bin/env python3
"""
Script para actualizar la base de datos con los nuevos campos del panel de administrador.
Este script agrega los nuevos campos a los modelos existentes sin perder datos.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, Vehicle, SystemActivity, MaintenanceRecord
from datetime import datetime
from sqlalchemy import text

def update_database():
    """Actualiza la base de datos con los nuevos campos del administrador."""
    app = create_app()
    
    with app.app_context():
        print("🔄 Actualizando base de datos con nuevos campos del administrador...")
        
        # Verificar si las tablas existen
        inspector = db.inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        # Crear tablas si no existen
        if 'system_activity' not in existing_tables:
            print("📝 Creando tabla system_activity...")
            SystemActivity.__table__.create(db.engine)
            print("✅ Tabla system_activity creada exitosamente")
        
        if 'maintenance_record' not in existing_tables:
            print("📝 Creando tabla maintenance_record...")
            MaintenanceRecord.__table__.create(db.engine)
            print("✅ Tabla maintenance_record creada exitosamente")
        
        # Verificar y agregar columnas faltantes en la tabla user
        user_columns = [col['name'] for col in inspector.get_columns('user')]
        
        if 'is_active' not in user_columns:
            print("📝 Agregando columna is_active a tabla user...")
            db.session.execute(text('ALTER TABLE user ADD COLUMN is_active BOOLEAN DEFAULT TRUE'))
            print("✅ Columna is_active agregada")
        
        if 'last_login' not in user_columns:
            print("📝 Agregando columna last_login a tabla user...")
            db.session.execute(text('ALTER TABLE user ADD COLUMN last_login DATETIME'))
            print("✅ Columna last_login agregada")
        
        if 'login_count' not in user_columns:
            print("📝 Agregando columna login_count a tabla user...")
            db.session.execute(text('ALTER TABLE user ADD COLUMN login_count INTEGER DEFAULT 0'))
            print("✅ Columna login_count agregada")
        
        if 'phone' not in user_columns:
            print("📝 Agregando columna phone a tabla user...")
            db.session.execute(text('ALTER TABLE user ADD COLUMN phone VARCHAR(20)'))
            print("✅ Columna phone agregada")
        
        # Verificar y agregar columnas faltantes en la tabla vehicle
        vehicle_columns = [col['name'] for col in inspector.get_columns('vehicle')]
        
        if 'maintenance_status' not in vehicle_columns:
            print("📝 Agregando columna maintenance_status a tabla vehicle...")
            db.session.execute(text('ALTER TABLE vehicle ADD COLUMN maintenance_status VARCHAR(20) DEFAULT "operational"'))
            print("✅ Columna maintenance_status agregada")
        
        if 'last_maintenance' not in vehicle_columns:
            print("📝 Agregando columna last_maintenance a tabla vehicle...")
            db.session.execute(text('ALTER TABLE vehicle ADD COLUMN last_maintenance DATETIME'))
            print("✅ Columna last_maintenance agregada")
        
        if 'next_maintenance' not in vehicle_columns:
            print("📝 Agregando columna next_maintenance a tabla vehicle...")
            db.session.execute(text('ALTER TABLE vehicle ADD COLUMN next_maintenance DATETIME'))
            print("✅ Columna next_maintenance agregada")
        
        if 'total_usage_hours' not in vehicle_columns:
            print("📝 Agregando columna total_usage_hours a tabla vehicle...")
            db.session.execute(text('ALTER TABLE vehicle ADD COLUMN total_usage_hours FLOAT DEFAULT 0'))
            print("✅ Columna total_usage_hours agregada")
        
        db.session.commit()
        
        # Actualizar usuarios existentes para que estén activos
        print("📝 Actualizando usuarios existentes...")
        users = User.query.all()
        for user in users:
            if not hasattr(user, 'is_active') or user.is_active is None:
                user.is_active = True
            if not hasattr(user, 'login_count') or user.login_count is None:
                user.login_count = 0
        
        db.session.commit()
        print(f"✅ {len(users)} usuarios actualizados")
        
        # Actualizar vehículos existentes
        print("📝 Actualizando vehículos existentes...")
        vehicles = Vehicle.query.all()
        for vehicle in vehicles:
            if not hasattr(vehicle, 'maintenance_status') or vehicle.maintenance_status is None:
                vehicle.maintenance_status = 'operational'
            if not hasattr(vehicle, 'total_usage_hours') or vehicle.total_usage_hours is None:
                vehicle.total_usage_hours = 0
        
        db.session.commit()
        print(f"✅ {len(vehicles)} vehículos actualizados")
        
        # Crear actividad inicial del sistema
        print("📝 Creando actividad inicial del sistema...")
        initial_activity = SystemActivity(
            user_id=None,
            action='system_startup',
            details='Sistema iniciado con nuevas funcionalidades de administrador',
            ip_address='127.0.0.1'
        )
        db.session.add(initial_activity)
        db.session.commit()
        print("✅ Actividad inicial creada")
        
        print("\n🎉 ¡Base de datos actualizada exitosamente!")
        print("\n📊 Resumen de cambios:")
        print("   • Nuevas tablas: system_activity, maintenance_record")
        print("   • Nuevos campos en user: is_active, last_login, login_count, phone")
        print("   • Nuevos campos en vehicle: maintenance_status, last_maintenance, next_maintenance, total_usage_hours")
        print("   • Usuarios existentes marcados como activos")
        print("   • Vehículos existentes marcados como operacionales")
        print("\n🚀 El panel de administrador está listo para usar.")

if __name__ == '__main__':
    try:
        update_database()
    except Exception as e:
        print(f"❌ Error al actualizar la base de datos: {e}")
        sys.exit(1) 