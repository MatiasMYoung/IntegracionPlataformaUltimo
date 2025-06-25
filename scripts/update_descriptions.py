from app import create_app, db
from app.models import Vehicle

def update_descriptions():
    app = create_app()
    with app.app_context():
        # Obtener todos los vehículos
        vehicles = Vehicle.query.all()
        
        updated_count = 0
        
        for vehicle in vehicles:
            # Agregar información sobre costo diario a cada descripción
            if "costo diario" not in vehicle.description.lower() and "precio diario" not in vehicle.description.lower():
                # Agregar la información del costo diario al final de la descripción
                vehicle.description += f" Costo de arriendo: ${vehicle.price_per_day:,.0f} por día."
                updated_count += 1
                print(f"Actualizado: {vehicle.name} {vehicle.model}")
        
        db.session.commit()
        print(f"\nResumen:")
        print(f"- Vehículos actualizados: {updated_count}")
        print(f"- Total de vehículos en el sistema: {len(vehicles)}")

if __name__ == '__main__':
    update_descriptions() 