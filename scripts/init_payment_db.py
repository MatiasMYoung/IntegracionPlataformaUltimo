#!/usr/bin/env python3
"""
Script para inicializar la base de datos con los nuevos modelos de pago
"""

import os
import sys
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Vehicle, Reservation, Notification, Payment

def init_database():
    """Inicializa la base de datos con los nuevos modelos"""
    app = create_app()
    
    with app.app_context():
        print("🔄 Inicializando base de datos...")
        
        try:
            # Eliminar todas las tablas existentes
            db.drop_all()
            print("✅ Tablas existentes eliminadas")
            
            # Crear todas las tablas
            db.create_all()
            print("✅ Nuevas tablas creadas")
            
            # Crear usuario administrador
            admin = User(
                username='admin',
                email='admin@example.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Crear usuario de prueba
            user = User(
                username='usuario',
                email='usuario@example.com',
                is_admin=False
            )
            user.set_password('usuario123')
            db.session.add(user)
            
            # Crear algunos vehículos de prueba
            vehiculos = [
                Vehicle(
                    name='Suzuki',
                    model='Swift',
                    year=2020,
                    fuel_efficiency=15.5,
                    price_per_day=25000,
                    category='vehiculo',
                    description='Vehículo compacto ideal para ciudad',
                    image_url='suzuki_swift.jpg'
                ),
                Vehicle(
                    name='Toyota',
                    model='Hilux',
                    year=2021,
                    fuel_efficiency=12.0,
                    price_per_day=45000,
                    category='vehiculo',
                    description='Pickup robusto para trabajo',
                    image_url='toyota_hilux.jpg'
                ),
                Vehicle(
                    name='Liebherr',
                    model='LTM 1100',
                    year=2019,
                    fuel_efficiency=8.5,
                    price_per_day=150000,
                    category='maquinaria',
                    description='Grúa telescópica de alta capacidad',
                    image_url='liebherr_ltm_1100.jpg'
                )
            ]
            
            for vehiculo in vehiculos:
                db.session.add(vehiculo)
            
            db.session.commit()
            print("✅ Datos de prueba creados")
            print("✅ Base de datos inicializada exitosamente!")
            
            print("\n📋 Credenciales de acceso:")
            print("👤 Administrador: admin / admin123")
            print("👤 Usuario: usuario / usuario123")
            
        except Exception as e:
            print(f"❌ Error inicializando la base de datos: {e}")
            db.session.rollback()
            return False
    
    return True

if __name__ == '__main__':
    init_database() 