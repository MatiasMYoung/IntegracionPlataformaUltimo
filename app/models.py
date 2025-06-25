from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))  # Campo de teléfono opcional
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)  # Para bloquear/desbloquear usuarios
    last_login = db.Column(db.DateTime)  # Último login del usuario
    login_count = db.Column(db.Integer, default=0)  # Contador de logins
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con reservas
    reservations = db.relationship('Reservation', backref='user', lazy='dynamic')
    # Relación con notificaciones
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')
    # Relación con actividad del sistema
    activities = db.relationship('SystemActivity', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    fuel_efficiency = db.Column(db.Float, nullable=False)  # km/litro
    price_per_day = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'vehiculo' o 'maquinaria'
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    available = db.Column(db.Boolean, default=True)
    maintenance_status = db.Column(db.String(20), default='operational')  # operational, maintenance, out_of_service
    last_maintenance = db.Column(db.DateTime)  # Última fecha de mantenimiento
    next_maintenance = db.Column(db.DateTime)  # Próxima fecha de mantenimiento programado
    total_usage_hours = db.Column(db.Float, default=0)  # Horas totales de uso
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con reservas
    reservations = db.relationship('Reservation', backref='vehicle', lazy='dynamic')
    # Relación con mantenimiento
    maintenance_records = db.relationship('MaintenanceRecord', backref='vehicle', lazy='dynamic')

    def __repr__(self):
        return f'<Vehicle {self.name} {self.model}>'

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, in_progress, cancelled, completed
    cancellation_reason = db.Column(db.Text)  # Motivo de cancelación
    cancelled_by_admin = db.Column(db.Boolean, default=False)  # Si fue cancelada por admin
    cancelled_at = db.Column(db.DateTime)  # Fecha de cancelación
    started_at = db.Column(db.DateTime)  # Fecha cuando se inició el uso
    completed_at = db.Column(db.DateTime)  # Fecha cuando se completó
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Campos de pago
    payment_status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed, refunded
    payment_token = db.Column(db.String(255))  # Token de Transbank
    payment_amount = db.Column(db.Float)  # Monto del pago
    payment_date = db.Column(db.DateTime)  # Fecha de pago exitoso
    transbank_transaction_id = db.Column(db.String(255))  # ID de transacción de Transbank
    payment_method = db.Column(db.String(50), default='webpay')  # webpay, transfer, etc.
    
    # Relación con pagos
    payments = db.relationship('Payment', backref='reservation_ref', lazy='dynamic')
    
    def __repr__(self):
        return f'<Reservation {self.id} - {self.user.username} - {self.vehicle.name}>'

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), default='info')  # info, warning, error, success
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Notification {self.id} - {self.user.username} - {self.title}>'

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed, refunded
    token = db.Column(db.String(255))  # Token de Transbank
    transbank_transaction_id = db.Column(db.String(255))  # ID de transacción de Transbank
    payment_method = db.Column(db.String(50), default='webpay')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)  # Fecha de completado
    error_message = db.Column(db.Text)  # Mensaje de error si falla
    transbank_response = db.Column(db.Text)  # JSON con respuesta completa de Transbank
    
    def __repr__(self):
        return f'<Payment {self.id} - Reservation {self.reservation_id} - {self.status}>'

class SystemActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Puede ser null si es actividad del sistema
    action = db.Column(db.String(100), nullable=False)  # login, logout, create_reservation, etc.
    details = db.Column(db.Text)  # Detalles adicionales de la acción
    ip_address = db.Column(db.String(45))  # Dirección IP del usuario
    user_agent = db.Column(db.Text)  # User agent del navegador
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SystemActivity {self.id} - {self.action} - {self.created_at}>'

class MaintenanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    maintenance_type = db.Column(db.String(50), nullable=False)  # preventive, corrective, emergency
    description = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Float)  # Costo del mantenimiento
    performed_by = db.Column(db.String(100))  # Quién realizó el mantenimiento
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)  # Fecha de finalización
    status = db.Column(db.String(20), default='scheduled')  # scheduled, in_progress, completed, cancelled
    notes = db.Column(db.Text)  # Notas adicionales
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<MaintenanceRecord {self.id} - {self.vehicle.name} - {self.maintenance_type}>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) 