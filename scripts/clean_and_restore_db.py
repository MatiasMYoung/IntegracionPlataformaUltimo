#!/usr/bin/env python3
"""
Script para limpiar la base de datos y restaurar los datos originales.
Elimina todos los usuarios excepto el administrador y restaura los vehículos y maquinaria originales.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, Vehicle, Reservation, Payment, Notification, SystemActivity, MaintenanceRecord
from datetime import datetime

def clean_and_restore_database():
    """Limpia la base de datos y restaura los datos originales."""
    app = create_app()
    
    with app.app_context():
        print("🧹 Limpiando base de datos...")
        
        # Eliminar todas las reservas, pagos, notificaciones y actividades
        print("📝 Eliminando reservas, pagos y notificaciones...")
        Reservation.query.delete()
        Payment.query.delete()
        Notification.query.delete()
        SystemActivity.query.delete()
        MaintenanceRecord.query.delete()
        
        # Eliminar todos los usuarios excepto el administrador
        print("📝 Eliminando usuarios (excepto administrador)...")
        admin_users = User.query.filter_by(is_admin=True).all()
        User.query.filter_by(is_admin=False).delete()
        
        # Si no hay administrador, crear uno
        if not admin_users:
            print("📝 Creando usuario administrador...")
            admin = User(
                username='admin',
                email='admin@salfa.cl',
                phone='+56 9 1234 5678',
                is_admin=True,
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            admin_users = [admin]
        
        # Eliminar todos los vehículos
        print("📝 Eliminando vehículos existentes...")
        Vehicle.query.delete()
        
        # Restaurar vehículos originales
        print("📝 Restaurando vehículos originales...")
        vehicles = [
            # Vehículos
            Vehicle(
                name='Suzuki Swift',
                model='GLX',
                year=2020,
                fuel_efficiency=18.5,
                price_per_day=25000,
                category='vehiculo',
                description='Automóvil compacto ideal para ciudad. Económico y fácil de manejar.',
                image_url='suzuki_swift.jpg',
                available=True,
                maintenance_status='operational'
            ),
            Vehicle(
                name='Toyota Hilux',
                model='4x4 Double Cab',
                year=2019,
                fuel_efficiency=12.0,
                price_per_day=45000,
                category='vehiculo',
                description='Pickup 4x4 robusto para trabajo pesado y terrenos difíciles.',
                image_url='toyota_hilux.jpg',
                available=True,
                maintenance_status='operational'
            ),
            Vehicle(
                name='Hyundai Grand i10',
                model='Premium',
                year=2021,
                fuel_efficiency=20.0,
                price_per_day=22000,
                category='vehiculo',
                description='Auto urbano compacto con excelente eficiencia de combustible.',
                image_url='hyundai_grand_i10.jpg',
                available=True,
                maintenance_status='operational'
            ),
            Vehicle(
                name='Hyundai H1',
                model='Van',
                year=2018,
                fuel_efficiency=14.5,
                price_per_day=35000,
                category='vehiculo',
                description='Van espaciosa para transporte de pasajeros o carga.',
                image_url='hyundai_h1.jpg',
                available=True,
                maintenance_status='operational'
            ),
            Vehicle(
                name='Hyundai i20',
                model='Active',
                year=2020,
                fuel_efficiency=19.0,
                price_per_day=23000,
                category='vehiculo',
                description='Hatchback moderno con tecnología avanzada.',
                image_url='hyundai_i20.jpg',
                available=True,
                maintenance_status='operational'
            ),
            Vehicle(
                name='Kia Rio',
                model='LX',
                year=2019,
                fuel_efficiency=18.0,
                price_per_day=24000,
                category='vehiculo',
                description='Sedán compacto con buen rendimiento y confort.',
                image_url='kia_rio.jpg',
                available=True,
                maintenance_status='operational'
            ),
            Vehicle(
                name='Mitsubishi L200',
                model='Triton',
                year=2018,
                fuel_efficiency=13.5,
                price_per_day=42000,
                category='vehiculo',
                description='Pickup 4x4 confiable para trabajo y aventura.',
                image_url='mitsubishi_l200.jpg',
                available=True,
                maintenance_status='operational'
            ),
            Vehicle(
                name='Volkswagen Voyage',
                model='Trendline',
                year=2020,
                fuel_efficiency=16.5,
                price_per_day=26000,
                category='vehiculo',
                description='Sedán familiar con excelente seguridad.',
                image_url='volkswagen_voyage.jpg',
                available=True,
                maintenance_status='operational'
            ),
            
            # Maquinaria
            Vehicle(
                name='Liebherr LTM 1100',
                model='Grúa Móvil',
                year=2017,
                fuel_efficiency=8.5,
                price_per_day=150000,
                category='maquinaria',
                description='Grúa móvil de 100 toneladas para proyectos de construcción pesada.',
                image_url='liebherr_ltm_1100.jpg',
                available=True,
                maintenance_status='operational'
            ),
            Vehicle(
                name='MAN TGS',
                model='Camión Volquete',
                year=2019,
                fuel_efficiency=10.0,
                price_per_day=80000,
                category='maquinaria',
                description='Camión volquete para transporte de materiales de construcción.',
                image_url='man_tgs.jpg',
                available=True,
                maintenance_status='operational'
            ),
            Vehicle(
                name='Marcopolo Paradiso',
                model='Bus Turístico',
                year=2018,
                fuel_efficiency=12.5,
                price_per_day=95000,
                category='maquinaria',
                description='Bus turístico de lujo para viajes corporativos y turismo.',
                image_url='marcopolo_paradiso.jpg',
                available=True,
                maintenance_status='operational'
            ),
            Vehicle(
                name='Mercedes-Benz Actros',
                model='Camión Carga',
                year=2020,
                fuel_efficiency=11.0,
                price_per_day=90000,
                category='maquinaria',
                description='Camión de carga pesada para logística y transporte.',
                image_url='mercedes_benz_actros.jpg',
                available=True,
                maintenance_status='operational'
            ),
            Vehicle(
                name='Mercedes-Benz Arocs',
                model='Camión Obra',
                year=2019,
                fuel_efficiency=10.5,
                price_per_day=85000,
                category='maquinaria',
                description='Camión especializado para obras de construcción.',
                image_url='mercedes_benz_arocs.jpg',
                available=True,
                maintenance_status='operational'
            ),
            Vehicle(
                name='Mercedes-Benz Sprinter',
                model='Furgón',
                year=2021,
                fuel_efficiency=15.0,
                price_per_day=35000,
                category='maquinaria',
                description='Furgón versátil para transporte de carga y pasajeros.',
                image_url='mercedes_benz_sprinter.jpg',
                available=True,
                maintenance_status='operational'
            ),
            Vehicle(
                name='Volvo B8RLE',
                model='Bus Urbano',
                year=2020,
                fuel_efficiency=13.0,
                price_per_day=70000,
                category='maquinaria',
                description='Bus urbano moderno para transporte público.',
                image_url='volvo_b8rle.jpg',
                available=True,
                maintenance_status='operational'
            ),
            Vehicle(
                name='Volvo FH',
                model='Camión Tráiler',
                year=2019,
                fuel_efficiency=9.5,
                price_per_day=120000,
                category='maquinaria',
                description='Camión tráiler para transporte de larga distancia.',
                image_url='volvo_fh.jpg',
                available=True,
                maintenance_status='operational'
            )
        ]
        
        for vehicle in vehicles:
            db.session.add(vehicle)
        
        # Crear actividad inicial
        print("📝 Creando actividad inicial...")
        initial_activity = SystemActivity(
            user_id=admin_users[0].id,
            action='database_restore',
            details='Base de datos limpiada y restaurada con datos originales',
            ip_address='127.0.0.1'
        )
        db.session.add(initial_activity)
        
        db.session.commit()
        
        print("\n🎉 ¡Base de datos limpiada y restaurada exitosamente!")
        print("\n📊 Resumen de cambios:")
        print(f"   • Usuarios eliminados (excepto administradores): {len(admin_users)} administradores conservados")
        print(f"   • Vehículos restaurados: {len(vehicles)} (8 vehículos + 8 maquinarias)")
        print("   • Todas las reservas, pagos y notificaciones eliminadas")
        print("   • Actividad del sistema reiniciada")
        print("\n🔑 Credenciales del administrador:")
        print("   • Usuario: admin")
        print("   • Contraseña: admin123")
        print("   • Email: admin@salfa.cl")
        print("\n🚀 El sistema está listo para usar.")

if __name__ == '__main__':
    try:
        clean_and_restore_database()
    except Exception as e:
        print(f"❌ Error al limpiar y restaurar la base de datos: {e}")
        sys.exit(1) 