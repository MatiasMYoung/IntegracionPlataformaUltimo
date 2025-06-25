#!/usr/bin/env python3
"""
Script para actualizar la base de datos con los nuevos campos de pago
"""

import os
import sys
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Reservation, Payment

def update_database():
    """Actualiza la base de datos con los nuevos campos de pago"""
    app = create_app()
    
    with app.app_context():
        print("🔄 Actualizando esquema de base de datos...")
        
        try:
            # Crear las nuevas tablas
            db.create_all()
            print("✅ Tablas creadas/actualizadas correctamente")
            
            # Verificar si hay reservas existentes y actualizar sus campos de pago
            reservations = Reservation.query.all()
            updated_count = 0
            
            for reservation in reservations:
                if reservation.payment_status is None:
                    reservation.payment_status = 'pending'
                    reservation.payment_method = 'webpay'
                    updated_count += 1
            
            if updated_count > 0:
                db.session.commit()
                print(f"✅ {updated_count} reservas actualizadas con campos de pago")
            else:
                print("ℹ️  No se encontraron reservas que necesiten actualización")
                
            print("🎉 Base de datos actualizada exitosamente!")
            
        except Exception as e:
            print(f"❌ Error al actualizar la base de datos: {e}")
            db.session.rollback()
            return False
    
    return True

if __name__ == '__main__':
    update_database() 