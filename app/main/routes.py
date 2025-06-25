from flask import render_template, flash, redirect, url_for, request, jsonify
from app.main import bp
from app.models import Vehicle, User, Reservation, Notification, Payment, SystemActivity, MaintenanceRecord
from app import db
import os
from app.utils.currency import convert_to_uf, convert_to_usd, format_currency
from flask_login import login_required, current_user, login_user, logout_user
from datetime import datetime, date, timedelta
from app.services.payment_service import PaymentService
from sqlalchemy import func, desc

@bp.route('/')
@bp.route('/index')
def index():
    vehicles = Vehicle.query.filter_by(available=True).all()
    return render_template('index.html', title='Inicio', vehicles=vehicles)

@bp.route('/vehiculos')
def vehiculos():
    vehicles = Vehicle.query.filter_by(category='vehiculo', available=True).all()
    return render_template('vehiculos.html', title='Vehículos', vehicles=vehicles, today=date.today().isoformat())

@bp.route('/maquinaria')
def maquinaria():
    machinery = Vehicle.query.filter_by(category='maquinaria', available=True).all()
    return render_template('maquinaria.html', title='Maquinaria', vehicles=machinery, today=date.today().isoformat())

@bp.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.index'))
    
    # Estadísticas para el dashboard
    stats = {
        'total_users': User.query.count(),
        'total_reservations': Reservation.query.count(),
        'total_vehicles': Vehicle.query.filter_by(available=True).count(),
        'pending_payments': Payment.query.filter_by(status='pending').count(),
        'active_reservations': Reservation.query.filter_by(status='in_progress').count(),
        'completed_reservations': Reservation.query.filter_by(status='completed').count(),
        'total_revenue': db.session.query(func.sum(Payment.amount)).filter_by(status='completed').scalar() or 0
    }
    
    # Actividad reciente (últimas 10 actividades)
    recent_activity = SystemActivity.query.order_by(desc(SystemActivity.created_at)).limit(10).all()
    
    return render_template('admin.html', stats=stats, recent_activity=recent_activity)

@bp.route('/admin/usuarios')
@login_required
def admin_usuarios():
    if not current_user.is_admin:
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.index'))
    
    usuarios = User.query.order_by(desc(User.created_at)).all()
    reservas = Reservation.query.order_by(desc(Reservation.created_at)).all()
    
    return render_template('admin_usuarios.html', usuarios=usuarios, reservas=reservas)

@bp.route('/admin/usuarios/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if not current_user.is_admin:
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        is_admin = 'is_admin' in request.form
        
        # Validaciones
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está en uso.', 'error')
            return redirect(url_for('main.add_user'))
        
        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado.', 'error')
            return redirect(url_for('main.add_user'))
        
        # Crear usuario
        user = User(
            username=username,
            email=email,
            phone=phone if phone else None,
            is_admin=is_admin
        )
        user.set_password(password)
        
        db.session.add(user)
        
        # Registrar actividad
        activity = SystemActivity(
            user_id=current_user.id,
            action='create_user',
            details=f'Usuario {username} creado por administrador',
            ip_address=request.remote_addr
        )
        db.session.add(activity)
        db.session.commit()
        
        flash(f'Usuario {username} creado exitosamente.', 'success')
        return redirect(url_for('main.admin_usuarios'))
    
    return render_template('user_form.html', user=None, action='Agregar')

@bp.route('/admin/usuarios/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin:
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        is_admin = 'is_admin' in request.form
        
        # Validaciones
        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != user.id:
            flash('El nombre de usuario ya está en uso.', 'error')
            return redirect(url_for('main.edit_user', user_id=user.id))
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email and existing_email.id != user.id:
            flash('El email ya está registrado.', 'error')
            return redirect(url_for('main.edit_user', user_id=user.id))
        
        # Actualizar usuario
        user.username = username
        user.email = email
        user.phone = phone if phone else None
        user.is_admin = is_admin
        
        # Si se proporcionó una nueva contraseña
        if request.form.get('password'):
            user.set_password(request.form['password'])
        
        # Registrar actividad
        activity = SystemActivity(
            user_id=current_user.id,
            action='edit_user',
            details=f'Usuario {username} editado por administrador',
            ip_address=request.remote_addr
        )
        db.session.add(activity)
        db.session.commit()
        
        flash(f'Usuario {username} actualizado exitosamente.', 'success')
        return redirect(url_for('main.admin_usuarios'))
    
    return render_template('user_form.html', user=user, action='Editar')

@bp.route('/admin/usuarios/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('No puedes eliminar tu propia cuenta.', 'danger')
        return redirect(url_for('main.admin_usuarios'))
    
    username = user.username
    
    # Eliminar usuario
    db.session.delete(user)
    
    # Registrar actividad
    activity = SystemActivity(
        user_id=current_user.id,
        action='delete_user',
        details=f'Usuario {username} eliminado por administrador',
        ip_address=request.remote_addr
    )
    db.session.add(activity)
    db.session.commit()
    
    flash(f'Usuario {username} eliminado exitosamente.', 'success')
    return redirect(url_for('main.admin_usuarios'))

@bp.route('/admin/usuarios/<int:user_id>/toggle-status', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    if not current_user.is_admin:
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('No puedes bloquear tu propia cuenta.', 'danger')
        return redirect(url_for('main.admin_usuarios'))
    
    user.is_active = not user.is_active
    status = 'activada' if user.is_active else 'bloqueada'
    
    # Registrar actividad
    activity = SystemActivity(
        user_id=current_user.id,
        action='toggle_user_status',
        details=f'Usuario {user.username} {status}',
        ip_address=request.remote_addr
    )
    db.session.add(activity)
    db.session.commit()
    
    flash(f'Usuario {user.username} {status} correctamente.', 'success')
    return redirect(url_for('main.admin_usuarios'))

@bp.route('/admin/usuarios/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
def toggle_admin_status(user_id):
    if not current_user.is_admin:
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('No puedes cambiar tu propio rol de administrador.', 'danger')
        return redirect(url_for('main.admin_usuarios'))
    
    user.is_admin = not user.is_admin
    status = 'administrador' if user.is_admin else 'usuario normal'
    
    # Registrar actividad
    activity = SystemActivity(
        user_id=current_user.id,
        action='toggle_admin_status',
        details=f'Usuario {user.username} cambiado a {status}',
        ip_address=request.remote_addr
    )
    db.session.add(activity)
    db.session.commit()
    
    flash(f'Usuario {user.username} ahora es {status}.', 'success')
    return redirect(url_for('main.admin_usuarios'))

@bp.route('/admin/usuarios/<int:user_id>/reset-password', methods=['POST'])
@login_required
def reset_user_password(user_id):
    if not current_user.is_admin:
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(user_id)
    new_password = 'password123'  # Contraseña temporal
    user.set_password(new_password)
    
    # Registrar actividad
    activity = SystemActivity(
        user_id=current_user.id,
        action='reset_password',
        details=f'Contraseña de {user.username} reseteada',
        ip_address=request.remote_addr
    )
    db.session.add(activity)
    db.session.commit()
    
    flash(f'Contraseña de {user.username} reseteada a: {new_password}', 'success')
    return redirect(url_for('main.admin_usuarios'))

@bp.route('/admin/vehiculos')
@login_required
def admin_vehiculos():
    if not current_user.is_admin:
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.index'))
    vehiculos = Vehicle.query.filter_by(category='vehiculo').all()
    maquinarias = Vehicle.query.filter_by(category='maquinaria').all()
    return render_template('admin_vehiculos.html', vehiculos=vehiculos, maquinarias=maquinarias)

@bp.route('/admin/reports')
@login_required
def admin_reports():
    if not current_user.is_admin:
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.index'))
    
    # Estadísticas para reportes
    total_revenue = db.session.query(func.sum(Payment.amount)).filter_by(status='completed').scalar() or 0
    monthly_revenue = db.session.query(func.sum(Payment.amount)).filter(
        Payment.status == 'completed',
        Payment.completed_at >= datetime.now().replace(day=1)
    ).scalar() or 0
    
    # Vehículos más rentables
    vehicle_revenue = db.session.query(
        Vehicle.name,
        Vehicle.model,
        func.sum(Payment.amount).label('total_revenue'),
        func.count(Payment.id).label('total_payments')
    ).join(Reservation).join(Payment).filter(
        Payment.status == 'completed'
    ).group_by(Vehicle.id).order_by(desc('total_revenue')).limit(5).all()
    
    # Reservas por estado
    reservations_by_status = db.session.query(
        Reservation.status,
        func.count(Reservation.id).label('count')
    ).group_by(Reservation.status).all()
    
    return render_template('admin_reports.html', 
                         total_revenue=total_revenue,
                         monthly_revenue=monthly_revenue,
                         vehicle_revenue=vehicle_revenue,
                         reservations_by_status=reservations_by_status)

@bp.route('/admin/maintenance')
@login_required
def admin_maintenance():
    if not current_user.is_admin:
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.index'))
    
    # Vehículos que necesitan mantenimiento
    vehicles_needing_maintenance = Vehicle.query.filter(
        (Vehicle.maintenance_status == 'maintenance') |
        (Vehicle.next_maintenance <= datetime.now() + timedelta(days=7))
    ).all()
    
    # Registros de mantenimiento recientes
    recent_maintenance = MaintenanceRecord.query.order_by(desc(MaintenanceRecord.created_at)).limit(10).all()
    
    return render_template('admin_maintenance.html', 
                         vehicles_needing_maintenance=vehicles_needing_maintenance,
                         recent_maintenance=recent_maintenance)

@bp.route('/admin/maintenance/add', methods=['GET', 'POST'])
@login_required
def add_maintenance():
    if not current_user.is_admin:
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        vehicle = Vehicle.query.get_or_404(request.form['vehicle_id'])
        
        maintenance = MaintenanceRecord(
            vehicle_id=vehicle.id,
            maintenance_type=request.form['maintenance_type'],
            description=request.form['description'],
            cost=float(request.form['cost']) if request.form['cost'] else None,
            performed_by=request.form['performed_by'],
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
            end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d') if request.form['end_date'] else None,
            status=request.form['status'],
            notes=request.form['notes']
        )
        
        # Actualizar estado del vehículo
        vehicle.maintenance_status = 'maintenance'
        vehicle.last_maintenance = maintenance.start_date
        
        db.session.add(maintenance)
        db.session.commit()
        
        flash('Mantenimiento registrado correctamente.', 'success')
        return redirect(url_for('main.admin_maintenance'))
    
    vehicles = Vehicle.query.all()
    return render_template('maintenance_form.html', vehicles=vehicles, today=date.today().isoformat())

@bp.route('/mis_reservas')
@login_required
def mis_reservas():
    # Obtener reservas del usuario ordenadas por fecha de creación
    reservas = current_user.reservations.order_by(Reservation.created_at.desc()).all()
    return render_template('mis_reservas.html', reservas=reservas)

# --- CRUD VEHÍCULOS ---
@bp.route('/vehiculos/add', methods=['GET', 'POST'])
@login_required
def add_vehiculo():
    if not current_user.is_admin:
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.index'))
    img_folder = os.path.join('app', 'static', 'img')
    images = [f for f in os.listdir(img_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if request.method == 'POST':
        v = Vehicle(
            name=request.form['name'],
            model=request.form['model'],
            year=int(request.form['year']),
            fuel_efficiency=float(request.form['fuel_efficiency']),
            price_per_day=float(request.form['price_per_day']),
            category='vehiculo',
            description=request.form['description'],
            image_url=request.form['image_url']
        )
        db.session.add(v)
        db.session.commit()
        flash('Vehículo agregado correctamente', 'success')
        return redirect(url_for('main.admin_vehiculos'))
    return render_template('vehiculo_form.html', images=images, action='Agregar', vehiculo=None)

@bp.route('/vehiculos/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_vehiculo(id):
    if not current_user.is_admin:
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.index'))
    vehiculo = Vehicle.query.get_or_404(id)
    img_folder = os.path.join('app', 'static', 'img')
    images = [f for f in os.listdir(img_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if request.method == 'POST':
        vehiculo.name = request.form['name']
        vehiculo.model = request.form['model']
        vehiculo.year = int(request.form['year'])
        vehiculo.fuel_efficiency = float(request.form['fuel_efficiency'])
        vehiculo.price_per_day = float(request.form['price_per_day'])
        vehiculo.description = request.form['description']
        vehiculo.image_url = request.form['image_url']
        db.session.commit()
        flash('Vehículo actualizado correctamente', 'success')
        return redirect(url_for('main.admin_vehiculos'))
    return render_template('vehiculo_form.html', images=images, action='Editar', vehiculo=vehiculo)

@bp.route('/vehiculos/delete/<int:id>', methods=['POST'])
@login_required
def delete_vehiculo(id):
    if not current_user.is_admin:
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.index'))
    vehiculo = Vehicle.query.get_or_404(id)
    db.session.delete(vehiculo)
    db.session.commit()
    flash('Vehículo eliminado correctamente', 'success')
    return redirect(url_for('main.admin_vehiculos'))

# --- CRUD MAQUINARIA ---
@bp.route('/maquinaria/add', methods=['GET', 'POST'])
@login_required
def add_maquinaria():
    if not current_user.is_admin:
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.index'))
    img_folder = os.path.join('app', 'static', 'img')
    images = [f for f in os.listdir(img_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if request.method == 'POST':
        m = Vehicle(
            name=request.form['name'],
            model=request.form['model'],
            year=int(request.form['year']),
            fuel_efficiency=float(request.form['fuel_efficiency']),
            price_per_day=float(request.form['price_per_day']),
            category='maquinaria',
            description=request.form['description'],
            image_url=request.form['image_url']
        )
        db.session.add(m)
        db.session.commit()
        flash('Maquinaria agregada correctamente', 'success')
        return redirect(url_for('main.admin_vehiculos'))
    return render_template('maquinaria_form.html', images=images, action='Agregar', maquinaria=None)

@bp.route('/maquinaria/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_maquinaria(id):
    if not current_user.is_admin:
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.index'))
    maquinaria = Vehicle.query.get_or_404(id)
    img_folder = os.path.join('app', 'static', 'img')
    images = [f for f in os.listdir(img_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if request.method == 'POST':
        maquinaria.name = request.form['name']
        maquinaria.model = request.form['model']
        maquinaria.year = int(request.form['year'])
        maquinaria.fuel_efficiency = float(request.form['fuel_efficiency'])
        maquinaria.price_per_day = float(request.form['price_per_day'])
        maquinaria.description = request.form['description']
        maquinaria.image_url = request.form['image_url']
        db.session.commit()
        flash('Maquinaria actualizada correctamente', 'success')
        return redirect(url_for('main.admin_vehiculos'))
    return render_template('maquinaria_form.html', images=images, action='Editar', maquinaria=maquinaria)

@bp.route('/maquinaria/delete/<int:id>', methods=['POST'])
@login_required
def delete_maquinaria(id):
    if not current_user.is_admin:
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.index'))
    maquinaria = Vehicle.query.get_or_404(id)
    db.session.delete(maquinaria)
    db.session.commit()
    flash('Maquinaria eliminada correctamente', 'success')
    return redirect(url_for('main.admin_vehiculos'))

@bp.route('/vehiculos/<int:vehicle_id>/reservar', methods=['POST'])
@login_required
def reservar_vehiculo(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    
    if not vehicle.available:
        flash('Este vehículo no está disponible para reserva.', 'error')
        return redirect(url_for('main.vehiculos'))
    
    start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
    
    # Validaciones
    if start_date < datetime.now():
        flash('La fecha de inicio no puede ser anterior a hoy.', 'error')
        return redirect(url_for('main.vehiculos'))
    
    if end_date <= start_date:
        flash('La fecha de fin debe ser posterior a la fecha de inicio.', 'error')
        return redirect(url_for('main.vehiculos'))
    
    # Calcular días y precio total
    days = (end_date - start_date).days
    total_price = days * vehicle.price_per_day
    
    # Verificar si hay conflictos de reserva
    existing_reservation = Reservation.query.filter(
        Reservation.vehicle_id == vehicle_id,
        Reservation.status.in_(['pending', 'confirmed']),
        Reservation.start_date <= end_date,
        Reservation.end_date >= start_date
    ).first()
    
    if existing_reservation:
        flash('Este vehículo ya está reservado para las fechas seleccionadas.', 'error')
        return redirect(url_for('main.vehiculos'))
    
    # Crear la reserva
    reservation = Reservation(
        user_id=current_user.id,
        vehicle_id=vehicle_id,
        start_date=start_date,
        end_date=end_date,
        total_price=total_price,
        status='pending',
        payment_status='pending'  # Agregar estado de pago pendiente
    )
    
    db.session.add(reservation)
    db.session.commit()
    
    flash(f'Reserva creada exitosamente. Total: {format_currency(total_price, "CLP")}. Proceda con el pago para confirmar.', 'success')
    return redirect(url_for('main.create_payment', reservation_id=reservation.id))

@bp.route('/maquinaria/<int:vehicle_id>/reservar', methods=['POST'])
@login_required
def reservar_maquinaria(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    
    if not vehicle.available:
        flash('Esta maquinaria no está disponible para reserva.', 'error')
        return redirect(url_for('main.maquinaria'))
    
    start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
    project_location = request.form['project_location']
    
    # Validaciones
    if start_date < datetime.now():
        flash('La fecha de inicio no puede ser anterior a hoy.', 'error')
        return redirect(url_for('main.maquinaria'))
    
    if end_date <= start_date:
        flash('La fecha de fin debe ser posterior a la fecha de inicio.', 'error')
        return redirect(url_for('main.maquinaria'))
    
    # Calcular días y precio total
    days = (end_date - start_date).days
    total_price = days * vehicle.price_per_day
    
    # Verificar si hay conflictos de reserva
    existing_reservation = Reservation.query.filter(
        Reservation.vehicle_id == vehicle_id,
        Reservation.status.in_(['pending', 'confirmed']),
        Reservation.start_date <= end_date,
        Reservation.end_date >= start_date
    ).first()
    
    if existing_reservation:
        flash('Esta maquinaria ya está reservada para las fechas seleccionadas.', 'error')
        return redirect(url_for('main.maquinaria'))
    
    # Crear la reserva
    reservation = Reservation(
        user_id=current_user.id,
        vehicle_id=vehicle_id,
        start_date=start_date,
        end_date=end_date,
        total_price=total_price,
        status='pending',
        payment_status='pending'  # Agregar estado de pago pendiente
    )
    
    db.session.add(reservation)
    db.session.commit()
    
    flash(f'Solicitud de maquinaria creada exitosamente. Total: {format_currency(total_price, "CLP")}. Proceda con el pago para confirmar.', 'success')
    return redirect(url_for('main.create_payment', reservation_id=reservation.id))

@bp.route('/admin/reservas')
@login_required
def admin_reservas():
    if not current_user.is_admin:
        flash('Acceso denegado. Solo administradores pueden ver esta página.', 'error')
        return redirect(url_for('main.index'))
    
    # Obtener todas las reservas ordenadas por fecha de creación
    reservas = Reservation.query.order_by(Reservation.created_at.desc()).all()
    return render_template('admin_reservas.html', reservas=reservas)

@bp.route('/admin/reservas/<int:reservation_id>/confirmar', methods=['POST'])
@login_required
def confirmar_reserva(reservation_id):
    if not current_user.is_admin:
        flash('Acceso denegado. Solo administradores pueden confirmar reservas.', 'error')
        return redirect(url_for('main.index'))
    
    reserva = Reservation.query.get_or_404(reservation_id)
    
    if reserva.status != 'pending':
        flash('Solo se pueden confirmar reservas pendientes.', 'error')
        return redirect(url_for('main.admin_reservas'))
    
    # Cambiar estado a confirmada
    reserva.status = 'confirmed'
    
    # Crear notificación para el usuario
    notificacion = Notification(
        user_id=reserva.user_id,
        title='Reserva Confirmada',
        message=f'Su reserva del vehículo "{reserva.vehicle.name}" ha sido confirmada.\n\nPuede retirar el vehículo en la fecha programada: {reserva.start_date.strftime("%d/%m/%Y %H:%M")}',
        type='success'
    )
    
    db.session.add(notificacion)
    db.session.commit()
    
    flash(f'Reserva #{reservation_id} confirmada exitosamente. Se ha enviado una notificación al usuario.', 'success')
    return redirect(url_for('main.admin_reservas'))

@bp.route('/admin/reservas/<int:reservation_id>/iniciar', methods=['POST'])
@login_required
def iniciar_reserva(reservation_id):
    if not current_user.is_admin:
        flash('Acceso denegado. Solo administradores pueden iniciar reservas.', 'error')
        return redirect(url_for('main.index'))
    
    reserva = Reservation.query.get_or_404(reservation_id)
    
    if reserva.status not in ['pending', 'confirmed']:
        flash('Solo se pueden iniciar reservas pendientes o confirmadas.', 'error')
        return redirect(url_for('main.admin_reservas'))
    
    # Cambiar estado a en curso
    reserva.status = 'in_progress'
    reserva.started_at = datetime.utcnow()
    
    # Crear notificación para el usuario
    notificacion = Notification(
        user_id=reserva.user_id,
        title='Uso Iniciado',
        message=f'El uso del vehículo "{reserva.vehicle.name}" ha sido iniciado.\n\nFecha de inicio: {reserva.started_at.strftime("%d/%m/%Y %H:%M")}',
        type='info'
    )
    
    db.session.add(notificacion)
    db.session.commit()
    
    flash(f'Reserva #{reservation_id} iniciada exitosamente. El vehículo está en uso.', 'success')
    return redirect(url_for('main.admin_reservas'))

@bp.route('/admin/reservas/<int:reservation_id>/completar', methods=['POST'])
@login_required
def completar_reserva(reservation_id):
    if not current_user.is_admin:
        flash('Acceso denegado. Solo administradores pueden completar reservas.', 'error')
        return redirect(url_for('main.index'))
    
    reserva = Reservation.query.get_or_404(reservation_id)
    
    if reserva.status != 'in_progress':
        flash('Solo se pueden completar reservas en curso.', 'error')
        return redirect(url_for('main.admin_reservas'))
    
    # Cambiar estado a completada
    reserva.status = 'completed'
    reserva.completed_at = datetime.utcnow()
    
    # Crear notificación para el usuario
    notificacion = Notification(
        user_id=reserva.user_id,
        title='Reserva Completada',
        message=f'El uso del vehículo "{reserva.vehicle.name}" ha sido completado.\n\nFecha de finalización: {reserva.completed_at.strftime("%d/%m/%Y %H:%M")}',
        type='success'
    )
    
    db.session.add(notificacion)
    db.session.commit()
    
    flash(f'Reserva #{reservation_id} completada exitosamente.', 'success')
    return redirect(url_for('main.admin_reservas'))

@bp.route('/admin/reservas/<int:reservation_id>/cancelar', methods=['GET', 'POST'])
@login_required
def cancelar_reserva(reservation_id):
    if not current_user.is_admin:
        flash('Acceso denegado. Solo administradores pueden cancelar reservas.', 'error')
        return redirect(url_for('main.index'))
    
    reserva = Reservation.query.get_or_404(reservation_id)
    
    if request.method == 'POST':
        motivo = request.form.get('motivo', 'Sin motivo especificado')
        
        # Actualizar estado de la reserva
        reserva.status = 'cancelled'
        reserva.cancellation_reason = motivo
        reserva.cancelled_by_admin = True
        reserva.cancelled_at = datetime.utcnow()
        
        # Crear notificación para el usuario
        notificacion = Notification(
            user_id=reserva.user_id,
            title='Reserva Cancelada',
            message=f'Su reserva del vehículo "{reserva.vehicle.name}" ha sido cancelada por el administrador.\n\nMotivo: {motivo}\n\nFecha de cancelación: {reserva.cancelled_at.strftime("%d/%m/%Y %H:%M")}',
            type='warning'
        )
        
        db.session.add(notificacion)
        db.session.commit()
        
        flash(f'Reserva #{reservation_id} cancelada exitosamente. Se ha enviado una notificación al usuario.', 'success')
        return redirect(url_for('main.admin_reservas'))
    
    return render_template('cancelar_reserva.html', reserva=reserva)

@bp.route('/notificaciones')
@login_required
def notificaciones():
    # Obtener notificaciones del usuario ordenadas por fecha
    notificaciones = current_user.notifications.order_by(Notification.created_at.desc()).all()
    return render_template('notificaciones.html', notificaciones=notificaciones)

@bp.route('/notificaciones/<int:notification_id>/marcar-leida')
@login_required
def marcar_notificacion_leida(notification_id):
    notificacion = Notification.query.get_or_404(notification_id)
    
    # Verificar que la notificación pertenece al usuario actual
    if notificacion.user_id != current_user.id:
        flash('Acceso denegado.', 'error')
        return redirect(url_for('main.notificaciones'))
    
    notificacion.read = True
    db.session.commit()
    
    return redirect(url_for('main.notificaciones'))

@bp.route('/notificaciones/marcar-todas-leidas')
@login_required
def marcar_todas_leidas():
    # Marcar todas las notificaciones del usuario como leídas
    current_user.notifications.filter_by(read=False).update({'read': True})
    db.session.commit()
    
    flash('Todas las notificaciones han sido marcadas como leídas.', 'success')
    return redirect(url_for('main.notificaciones'))

@bp.context_processor
def utility_processor():
    def format_currency(amount, currency='CLP'):
        if currency == 'CLP':
            return f"${amount:,.0f} CLP"
        elif currency == 'USD':
            return f"US${amount:,.2f}"
        elif currency == 'UF':
            return f"{amount:,.2f} UF"
        else:
            return f"{amount:,.2f} {currency}"
    
    def nl2br(text):
        if text:
            return text.replace('\n', '<br>')
        return text
    
    return {
        'convert_to_uf': convert_to_uf,
        'convert_to_usd': convert_to_usd,
        'format_currency': format_currency,
        'nl2br': nl2br
    }

# --- RUTAS DE PAGO ---
@bp.route('/payment/create/<int:reservation_id>')
@login_required
def create_payment(reservation_id):
    """Inicia el proceso de pago para una reserva"""
    reservation = Reservation.query.get_or_404(reservation_id)
    
    # Verificar que la reserva pertenece al usuario actual
    if reservation.user_id != current_user.id:
        flash('No tienes permisos para acceder a esta reserva.', 'error')
        return redirect(url_for('main.mis_reservas'))
    
    # Verificar que la reserva esté pendiente de pago o fallida (para reintentar)
    if reservation.payment_status not in ['pending', 'failed']:
        flash('Esta reserva ya no está pendiente de pago.', 'error')
        return redirect(url_for('main.mis_reservas'))
    
    try:
        payment_service = PaymentService()
        success, message, response = payment_service.create_payment(reservation)
        
        if success:
            # Mostrar template con enlace y redirect a Webpay
            return render_template('payment_redirect.html', url=response['url'], token=response['token'])
        else:
            flash(f'Error al crear el pago: {message}', 'error')
            return redirect(url_for('main.mis_reservas'))
            
    except Exception as e:
        flash(f'Error inesperado: {str(e)}', 'error')
        return redirect(url_for('main.mis_reservas'))

@bp.route('/payment/return')
def payment_return():
    """URL de retorno después del pago en Webpay"""
    token = request.args.get('token_ws')
    
    if not token:
        flash('Token de pago no válido.', 'error')
        return redirect(url_for('main.mis_reservas'))
    
    try:
        payment_service = PaymentService()
        success, message, response = payment_service.confirm_payment(token)
        
        if success:
            flash('¡Pago procesado exitosamente! Tu reserva ha sido confirmada.', 'success')
        else:
            flash(f'Error en el pago: {message}', 'error')
            
    except Exception as e:
        flash(f'Error inesperado procesando el pago: {str(e)}', 'error')
    
    return redirect(url_for('main.mis_reservas'))

@bp.route('/payment/status/<int:reservation_id>')
@login_required
def payment_status(reservation_id):
    """Consulta el estado de pago de una reserva"""
    reservation = Reservation.query.get_or_404(reservation_id)
    
    # Verificar que la reserva pertenece al usuario actual
    if reservation.user_id != current_user.id:
        flash('No tienes permisos para acceder a esta reserva.', 'error')
        return redirect(url_for('main.mis_reservas'))
    
    payment = Payment.query.filter_by(reservation_id=reservation_id).first()
    
    return render_template('payment_status.html', reservation=reservation, payment=payment)

@bp.route('/admin/payments')
@login_required
def admin_payments():
    """Panel de administración de pagos"""
    if not current_user.is_admin:
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.index'))
    
    payments = Payment.query.order_by(Payment.created_at.desc()).all()
    return render_template('admin_payments.html', payments=payments)

@bp.route('/admin/payments/<int:payment_id>/refund', methods=['POST'])
@login_required
def refund_payment(payment_id):
    """Procesa un reembolso"""
    if not current_user.is_admin:
        flash('Acceso restringido solo para administradores.', 'danger')
        return redirect(url_for('main.index'))
    
    payment = Payment.query.get_or_404(payment_id)
    
    if payment.status != 'completed':
        flash('Solo se pueden reembolsar pagos completados.', 'error')
        return redirect(url_for('main.admin_payments'))
    
    try:
        payment_service = PaymentService()
        success, message, response = payment_service.refund_payment(payment.token, payment.amount)
        
        if success:
            flash('Reembolso procesado exitosamente.', 'success')
        else:
            flash(f'Error procesando reembolso: {message}', 'error')
            
    except Exception as e:
        flash(f'Error inesperado: {str(e)}', 'error')
    
    return redirect(url_for('main.admin_payments')) 