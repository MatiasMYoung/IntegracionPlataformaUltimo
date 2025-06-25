import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Configuración básica
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-que-deberias-cambiar'
    
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de Transbank
    TRANSBANK_COMMERCE_CODE = os.environ.get('TRANSBANK_COMMERCE_CODE') or '597055555532'
    TRANSBANK_API_KEY = os.environ.get('TRANSBANK_API_KEY') or '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'
    TRANSBANK_ENVIRONMENT = os.environ.get('TRANSBANK_ENVIRONMENT') or 'TEST'
    TRANSBANK_RETURN_URL = os.environ.get('TRANSBANK_RETURN_URL') or 'http://127.0.0.1:5000/payment/return' 