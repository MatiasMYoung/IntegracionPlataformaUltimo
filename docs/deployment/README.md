# 🚀 Guía de Despliegue - Sistema Salfa

## 📋 Índice

1. [Introducción](#-introducción)
2. [Requisitos del Servidor](#-requisitos-del-servidor)
3. [Preparación del Entorno](#-preparación-del-entorno)
4. [Configuración de Base de Datos](#-configuración-de-base-de-datos)
5. [Configuración de Transbank](#-configuración-de-transbank)
6. [Despliegue con Gunicorn](#-despliegue-con-gunicorn)
7. [Configuración de Nginx](#-configuración-de-nginx)
8. [Configuración de SSL/HTTPS](#-configuración-de-sslhttps)
9. [Configuración de Logging](#-configuración-de-logging)
10. [Backup y Mantenimiento](#-backup-y-mantenimiento)
11. [Monitoreo](#-monitoreo)
12. [Solución de Problemas](#-solución-de-problemas)

## 🎯 Introducción

Esta guía te ayudará a desplegar el Sistema Salfa en un entorno de producción seguro y escalable. El sistema está diseñado para funcionar con Flask, pero en producción usaremos Gunicorn como servidor WSGI y Nginx como proxy inverso.

## 🖥️ Requisitos del Servidor

### Especificaciones Mínimas

- **CPU**: 2 cores
- **RAM**: 4 GB
- **Almacenamiento**: 20 GB SSD
- **Sistema Operativo**: Ubuntu 20.04 LTS o superior

### Especificaciones Recomendadas

- **CPU**: 4+ cores
- **RAM**: 8+ GB
- **Almacenamiento**: 50+ GB SSD
- **Sistema Operativo**: Ubuntu 22.04 LTS

### Software Requerido

- **Python**: 3.8+
- **Nginx**: 1.18+
- **PostgreSQL**: 12+ (recomendado) o MySQL 8+
- **Redis**: 6+ (opcional, para cache)
- **Certbot**: Para certificados SSL

## 🔧 Preparación del Entorno

### 1. Actualizar el Sistema

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Instalar Dependencias del Sistema

```bash
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib redis-server git curl wget unzip
```

### 3. Crear Usuario para la Aplicación

```bash
sudo adduser salfa
sudo usermod -aG sudo salfa
sudo su - salfa
```

### 4. Clonar el Repositorio

```bash
cd /home/salfa
git clone <url-del-repositorio> salfa-app
cd salfa-app
```

### 5. Crear Entorno Virtual

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Instalar Gunicorn

```bash
pip install gunicorn
```

## 🗄️ Configuración de Base de Datos

### Opción 1: PostgreSQL (Recomendado)

#### 1. Configurar PostgreSQL

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE salfa_db;
CREATE USER salfa_user WITH PASSWORD 'tu_password_seguro';
GRANT ALL PRIVILEGES ON DATABASE salfa_db TO salfa_user;
\q
```

#### 2. Instalar Driver de PostgreSQL

```bash
pip install psycopg2-binary
```

#### 3. Configurar Conexión

Editar `config.py`:

```python
DATABASE_URL = "postgresql://salfa_user:tu_password_seguro@localhost/salfa_db"
```

### Opción 2: MySQL

#### 1. Configurar MySQL

```bash
sudo mysql_secure_installation
sudo mysql -u root -p
```

```sql
CREATE DATABASE salfa_db;
CREATE USER 'salfa_user'@'localhost' IDENTIFIED BY 'tu_password_seguro';
GRANT ALL PRIVILEGES ON salfa_db.* TO 'salfa_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 2. Instalar Driver de MySQL

```bash
pip install mysqlclient
```

#### 3. Configurar Conexión

```python
DATABASE_URL = "mysql://salfa_user:tu_password_seguro@localhost/salfa_db"
```

### 3. Inicializar Base de Datos

```bash
python scripts/init_payment_db.py
python scripts/init_admin.py
```

## 💳 Configuración de Transbank

### 1. Obtener Credenciales de Producción

Contacta a Transbank para obtener:
- **Commerce Code** de producción
- **API Key** de producción
- **Certificados** SSL (si aplica)

### 2. Configurar Variables de Entorno

Crear archivo `.env`:

```bash
# Transbank Producción
TRANSBANK_COMMERCE_CODE="tu_commerce_code_produccion"
TRANSBANK_API_KEY="tu_api_key_produccion"
TRANSBANK_ENVIRONMENT="LIVE"
TRANSBANK_RETURN_URL="https://tu-dominio.com/payment/return"

# Aplicación
SECRET_KEY="tu_clave_secreta_muy_larga_y_segura"
FLASK_ENV="production"
DATABASE_URL="postgresql://salfa_user:password@localhost/salfa_db"

# Logging
LOG_LEVEL="INFO"
LOG_FILE="/var/log/salfa/app.log"
```

### 3. Actualizar Configuración

Editar `config.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Transbank
    TRANSBANK_COMMERCE_CODE = os.environ.get('TRANSBANK_COMMERCE_CODE')
    TRANSBANK_API_KEY = os.environ.get('TRANSBANK_API_KEY')
    TRANSBANK_ENVIRONMENT = os.environ.get('TRANSBANK_ENVIRONMENT', 'TEST')
    TRANSBANK_RETURN_URL = os.environ.get('TRANSBANK_RETURN_URL')
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', '/var/log/salfa/app.log')
```

## 🚀 Despliegue con Gunicorn

### 1. Crear Archivo de Configuración de Gunicorn

Crear `gunicorn.conf.py`:

```python
# Gunicorn configuration file
import multiprocessing

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/var/log/salfa/gunicorn_access.log"
errorlog = "/var/log/salfa/gunicorn_error.log"
loglevel = "info"

# Process naming
proc_name = "salfa"

# Server mechanics
daemon = False
pidfile = "/var/run/salfa/gunicorn.pid"
user = "salfa"
group = "salfa"
tmp_upload_dir = None
```

### 2. Crear Servicio Systemd

Crear `/etc/systemd/system/salfa.service`:

```ini
[Unit]
Description=Salfa Gunicorn daemon
After=network.target

[Service]
User=salfa
Group=salfa
WorkingDirectory=/home/salfa/salfa-app
Environment="PATH=/home/salfa/salfa-app/venv/bin"
ExecStart=/home/salfa/salfa-app/venv/bin/gunicorn --config gunicorn.conf.py run:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### 3. Crear Directorios de Logs

```bash
sudo mkdir -p /var/log/salfa
sudo mkdir -p /var/run/salfa
sudo chown -R salfa:salfa /var/log/salfa /var/run/salfa
```

### 4. Iniciar el Servicio

```bash
sudo systemctl daemon-reload
sudo systemctl enable salfa
sudo systemctl start salfa
sudo systemctl status salfa
```

## 🌐 Configuración de Nginx

### 1. Crear Configuración de Nginx

Crear `/etc/nginx/sites-available/salfa`:

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;
    
    # Redirigir a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com www.tu-dominio.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Logs
    access_log /var/log/nginx/salfa_access.log;
    error_log /var/log/nginx/salfa_error.log;
    
    # Client max body size
    client_max_body_size 10M;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied expired no-cache no-store private must-revalidate auth;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss;
    
    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    # Static files
    location /static/ {
        alias /home/salfa/salfa-app/app/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Health check
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

### 2. Habilitar el Sitio

```bash
sudo ln -s /etc/nginx/sites-available/salfa /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🔒 Configuración de SSL/HTTPS

### 1. Instalar Certbot

```bash
sudo apt install certbot python3-certbot-nginx
```

### 2. Obtener Certificado SSL

```bash
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

### 3. Configurar Renovación Automática

```bash
sudo crontab -e
```

Agregar línea:

```
0 12 * * * /usr/bin/certbot renew --quiet
```

## 📝 Configuración de Logging

### 1. Configurar Logrotate

Crear `/etc/logrotate.d/salfa`:

```
/var/log/salfa/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 salfa salfa
    postrotate
        systemctl reload salfa
    endscript
}
```

### 2. Configurar Logging en la Aplicación

Editar `app/__init__.py`:

```python
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configurar logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/salfa.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Salfa startup')
    
    return app
```

## 💾 Backup y Mantenimiento

### 1. Script de Backup

Crear `scripts/backup.sh`:

```bash
#!/bin/bash

# Configuración
BACKUP_DIR="/backup/salfa"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="salfa_db"
DB_USER="salfa_user"

# Crear directorio de backup
mkdir -p $BACKUP_DIR

# Backup de base de datos
pg_dump -U $DB_USER $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# Backup de archivos estáticos
tar -czf $BACKUP_DIR/static_backup_$DATE.tar.gz app/static/

# Backup de configuración
tar -czf $BACKUP_DIR/config_backup_$DATE.tar.gz config.py .env

# Limpiar backups antiguos (mantener últimos 7 días)
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completado: $DATE"
```

### 2. Configurar Backup Automático

```bash
sudo crontab -e
```

Agregar línea:

```
0 2 * * * /home/salfa/salfa-app/scripts/backup.sh
```

### 3. Script de Mantenimiento

Crear `scripts/maintenance.sh`:

```bash
#!/bin/bash

# Actualizar código
cd /home/salfa/salfa-app
git pull origin main

# Actualizar dependencias
source venv/bin/activate
pip install -r requirements.txt

# Reiniciar servicios
sudo systemctl restart salfa
sudo systemctl reload nginx

echo "Mantenimiento completado"
```

## 📊 Monitoreo

### 1. Instalar Herramientas de Monitoreo

```bash
sudo apt install htop iotop nethogs
```

### 2. Configurar Monitoreo de Servicios

Crear script de monitoreo:

```bash
#!/bin/bash

# Verificar servicios
if ! systemctl is-active --quiet salfa; then
    echo "Salfa service is down!"
    systemctl restart salfa
fi

if ! systemctl is-active --quiet nginx; then
    echo "Nginx service is down!"
    systemctl restart nginx
fi

# Verificar espacio en disco
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "Disk usage is high: ${DISK_USAGE}%"
fi
```

### 3. Configurar Alertas

```bash
sudo crontab -e
```

Agregar línea:

```
*/5 * * * * /home/salfa/salfa-app/scripts/monitor.sh
```

## 🛠️ Solución de Problemas

### Problemas Comunes

#### 1. Servicio no inicia

```bash
# Verificar logs
sudo journalctl -u salfa -f

# Verificar configuración
sudo systemctl status salfa
```

#### 2. Error de permisos

```bash
# Corregir permisos
sudo chown -R salfa:salfa /home/salfa/salfa-app
sudo chmod -R 755 /home/salfa/salfa-app
```

#### 3. Base de datos no conecta

```bash
# Verificar conexión
sudo -u postgres psql -d salfa_db -c "SELECT 1;"

# Verificar variables de entorno
echo $DATABASE_URL
```

#### 4. Nginx no sirve archivos estáticos

```bash
# Verificar configuración
sudo nginx -t

# Verificar permisos
sudo chown -R www-data:www-data /home/salfa/salfa-app/app/static
```

### Comandos Útiles

```bash
# Reiniciar servicios
sudo systemctl restart salfa nginx

# Ver logs en tiempo real
sudo tail -f /var/log/salfa/gunicorn_error.log
sudo tail -f /var/log/nginx/salfa_error.log

# Verificar puertos
sudo netstat -tlnp | grep :8000
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :443

# Verificar SSL
sudo certbot certificates
```

## 🔄 Actualizaciones

### Proceso de Actualización

1. **Crear backup** antes de actualizar
2. **Pausar servicios** temporalmente
3. **Actualizar código** y dependencias
4. **Ejecutar migraciones** de base de datos
5. **Reiniciar servicios**
6. **Verificar funcionamiento**

### Script de Actualización

```bash
#!/bin/bash

echo "Iniciando actualización..."

# Backup
./scripts/backup.sh

# Pausar servicios
sudo systemctl stop salfa

# Actualizar código
git pull origin main

# Actualizar dependencias
source venv/bin/activate
pip install -r requirements.txt

# Migraciones (si las hay)
python scripts/update_payment_schema.py

# Reiniciar servicios
sudo systemctl start salfa

echo "Actualización completada"
```

---

**Versión de la guía:** 1.0.0  
**Última actualización:** Junio 2025  
**Para soporte técnico:** [soporte@salfa.cl] 