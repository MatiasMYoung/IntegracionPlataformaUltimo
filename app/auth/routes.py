from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse
from app.auth import bp
from app.models import User, SystemActivity
from app import db
from datetime import datetime

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            flash('Usuario o contraseña incorrectos', 'error')
            return redirect(url_for('auth.login'))
        
        # Verificar si el usuario está bloqueado
        if not user.is_active:
            flash('Tu cuenta ha sido bloqueada. Contacta al administrador.', 'error')
            return redirect(url_for('auth.login'))
        
        # Actualizar datos de login
        user.last_login = datetime.utcnow()
        user.login_count += 1
        
        # Registrar actividad
        activity = SystemActivity(
            user_id=user.id,
            action='login',
            details=f'Login exitoso desde {request.remote_addr}',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        
        db.session.add(activity)
        db.session.commit()
        
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.index')
        
        flash(f'Bienvenido, {user.username}!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Iniciar Sesión')

@bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        # Registrar actividad de logout
        activity = SystemActivity(
            user_id=current_user.id,
            action='logout',
            details=f'Logout desde {request.remote_addr}',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(activity)
        db.session.commit()
    
    logout_user()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form.get('phone')  # Campo opcional
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está en uso', 'error')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'error')
            return redirect(url_for('auth.register'))
        
        user = User(username=username, email=email, phone=phone if phone else None)
        user.set_password(password)
        db.session.add(user)
        
        # Registrar actividad de registro
        activity = SystemActivity(
            user_id=user.id,
            action='register',
            details=f'Nuevo usuario registrado desde {request.remote_addr}',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(activity)
        db.session.commit()
        
        flash('Usuario registrado correctamente. Puedes iniciar sesión ahora.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Registrarse') 