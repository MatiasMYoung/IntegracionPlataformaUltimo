# -*- coding: utf-8 -*-
"""
Archivo de configuración de ejemplo para el Sistema Salfa
Copia este archivo como 'config.py' y edita las variables según tu entorno
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env
load_dotenv()

class Config:
    """Configuración base de la aplicación"""
    
    # Configuración de seguridad
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cambia-esta-clave-en-produccion'
    
    # Configuración de base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///instance/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de Transbank
    TRANSBANK_COMMERCE_CODE = os.environ.get('TRANSBANK_COMMERCE_CODE') or '597055555532'
    TRANSBANK_API_KEY = os.environ.get('TRANSBANK_API_KEY') or '0208f0a6fa6a6a1a1a1a1a1a1a1a1a1a'
    TRANSBANK_ENVIRONMENT = os.environ.get('TRANSBANK_ENVIRONMENT') or 'TEST'
    TRANSBANK_RETURN_URL = os.environ.get('TRANSBANK_RETURN_URL') or 'http://127.0.0.1:5000/payment/return'
    
    # Configuración de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.environ.get('LOG_FILE') or 'logs/salfa.log'
    
    # Configuración de la aplicación
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # Configuración de archivos
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'app/static/img'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Configuración de paginación
    ITEMS_PER_PAGE = 12
    
    # Configuración de sesión
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hora
    
    # Configuración de correo (futuro)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Configuración de Redis (opcional, para cache)
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    
    # En producción, asegúrate de que estas variables estén configuradas
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY debe estar configurada en producción")
    
    # Configuración de base de datos para producción
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL debe estar configurada en producción")
    
    # Configuración de Transbank para producción
    TRANSBANK_ENVIRONMENT = 'LIVE'
    TRANSBANK_COMMERCE_CODE = os.environ.get('TRANSBANK_COMMERCE_CODE')
    TRANSBANK_API_KEY = os.environ.get('TRANSBANK_API_KEY')
    TRANSBANK_RETURN_URL = os.environ.get('TRANSBANK_RETURN_URL')
    
    if not all([TRANSBANK_COMMERCE_CODE, TRANSBANK_API_KEY, TRANSBANK_RETURN_URL]):
        raise ValueError("Todas las variables de Transbank deben estar configuradas en producción")

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Función para obtener la configuración según el entorno
def get_config():
    """Retorna la configuración según el entorno"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default']) 