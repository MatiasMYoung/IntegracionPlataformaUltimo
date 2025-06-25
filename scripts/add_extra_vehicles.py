from app import create_app, db
from app.models import Vehicle

def add_extra_vehicles():
    app = create_app()
    with app.app_context():
        # Verificar si ya existen estos vehículos
        cania = Vehicle.query.filter_by(model='Serie R').first()
        hilux = Vehicle.query.filter_by(model='Hilux').first()
        if cania:
            print('Cania Serie R ya existe en la base de datos.')
        else:
            cania = Vehicle(
                name='Cania',
                model='Serie R',
                year=2022,
                fuel_efficiency=7.5,
                price_per_day=170000,
                category='maquinaria',
                description='Camión de alto tonelaje para transporte pesado.',
                image_url='cania_serie_r.jpg',
                available=True
            )
            db.session.add(cania)
            print('Cania Serie R agregado.')
        if hilux:
            print('Toyota Hilux ya existe en la base de datos.')
        else:
            hilux = Vehicle(
                name='Toyota',
                model='Hilux',
                year=2023,
                fuel_efficiency=13.5,
                price_per_day=49000,
                category='vehiculo',
                description='Pickup confiable y versátil para todo tipo de terreno.',
                image_url='toyota_hilux.jpg',
                available=True
            )
            db.session.add(hilux)
            print('Toyota Hilux agregada.')
        db.session.commit()
        print('Vehículos extra agregados correctamente.')

if __name__ == '__main__':
    add_extra_vehicles() 