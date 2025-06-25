# 📁 Estructura del Proyecto - Sistema Salfa

## 🎯 Resumen de la Reorganización

El proyecto ha sido reorganizado para mejorar la documentación, mantenimiento y escalabilidad. A continuación se describe la nueva estructura y los cambios realizados.

## 📂 Estructura de Carpetas

```
Integracion/
├── 📁 app/                           # Aplicación principal Flask
│   ├── 📁 auth/                      # Autenticación y autorización
│   ├── 📁 main/                      # Rutas principales
│   ├── 📁 services/                  # Servicios de negocio
│   ├── 📁 static/                    # Archivos estáticos
│   │   ├── 📁 css/                   # Estilos CSS
│   │   ├── 📁 js/                    # JavaScript
│   │   └── 📁 img/                   # Imágenes
│   │       └── 📁 Fotos integracion/ # Imágenes movidas aquí
│   ├── 📁 templates/                 # Templates HTML
│   └── 📁 utils/                     # Utilidades
├── 📁 docs/                          # 📚 DOCUMENTACIÓN
│   ├── 📁 api/                       # Documentación de API
│   ├── 📁 deployment/                # Guías de despliegue
│   ├── 📁 user_guide/                # Manual de usuario
│   ├── 📄 Credenciales BDE.txt       # Credenciales movidas aquí
│   ├── 📄 bancoCentral.ipynb         # Notebooks movidos aquí
│   └── 📄 API_UF (1).ipynb           # Notebooks movidos aquí
├── 📁 scripts/                       # 🛠️ SCRIPTS DE MANTENIMIENTO
│   ├── 📄 init_payment_db.py         # Inicializar BD con pagos
│   ├── 📄 init_admin.py              # Crear usuario admin
│   ├── 📄 init_sample_data.py        # Cargar datos de ejemplo
│   ├── 📄 update_payment_schema.py   # Actualizar esquema pagos
│   ├── 📄 update_db_schema.py        # Actualizar esquema BD
│   ├── 📄 init_db.py                 # Inicializar BD básica
│   ├── 📄 check_db.py                # Verificar BD
│   └── 📄 check_db_path.py           # Verificar rutas BD
├── 📁 tests/                         # 🧪 TESTS (preparado para futuro)
├── 📁 venv/                          # Entorno virtual Python
├── 📄 README.md                      # 📖 Documentación principal
├── 📄 config.example.py              # 🔧 Configuración de ejemplo
├── 📄 env.example                    # 🔐 Variables de entorno ejemplo
├── 📄 requirements.txt               # 📦 Dependencias (incluye transbank-sdk)
├── 📄 run.py                         # 🚀 Script de ejecución
└── 📄 .gitignore                     # 🚫 Archivos ignorados por Git
```

## 🔄 Cambios Realizados

### 1. **Reorganización de Documentación** (`docs/`)
- ✅ **Creada carpeta `docs/`** para toda la documentación
- ✅ **Subcarpetas organizadas:**
  - `api/` - Documentación técnica de la API
  - `deployment/` - Guías de despliegue en producción
  - `user_guide/` - Manual completo de usuario
- ✅ **Archivos movidos:**
  - `Credenciales BDE.txt` → `docs/`
  - `bancoCentral.ipynb` → `docs/`
  - `API_UF (1).ipynb` → `docs/`

### 2. **Organización de Scripts** (`scripts/`)
- ✅ **Creada carpeta `scripts/`** para todos los scripts de mantenimiento
- ✅ **Scripts organizados por función:**
  - Inicialización de BD
  - Actualización de esquemas
  - Verificación de sistema
  - Carga de datos

### 3. **Reorganización de Imágenes**
- ✅ **Imágenes movidas** de `Fotos integracion/` a `app/static/img/Fotos integracion/`
- ✅ **Estructura más lógica** para archivos estáticos

### 4. **Limpieza del Proyecto**
- ✅ **Eliminada carpeta `transbank-sdk-python-master/`** - No era necesaria
- ✅ **SDK instalado via pip** - Usando `transbank-sdk>=1.0.0` en requirements.txt
- ✅ **Proyecto más limpio** - Sin código fuente duplicado

### 5. **Documentación Mejorada**
- ✅ **README.md completamente reescrito** con estructura profesional
- ✅ **Documentación de API** completa en `docs/api/README.md`
- ✅ **Manual de usuario** detallado en `docs/user_guide/README.md`
- ✅ **Guía de despliegue** completa en `docs/deployment/README.md`

### 6. **Archivos de Configuración**
- ✅ **`config.example.py`** - Configuración de ejemplo
- ✅ **`env.example`** - Variables de entorno de ejemplo
- ✅ **Documentación de configuración** mejorada

## 📚 Documentación Disponible

### 1. **README Principal** (`README.md`)
- Descripción completa del proyecto
- Instrucciones de instalación
- Configuración básica
- Guía de uso rápida
- Enlaces a documentación detallada

### 2. **Documentación de API** (`docs/api/README.md`)
- Todos los endpoints disponibles
- Parámetros y respuestas
- Estructura de datos
- Estados del sistema
- Configuración de seguridad

### 3. **Manual de Usuario** (`docs/user_guide/README.md`)
- Guía paso a paso para usuarios
- Proceso de registro y login
- Cómo crear reservas
- Sistema de pagos
- Panel de administración
- Solución de problemas

### 4. **Guía de Despliegue** (`docs/deployment/README.md`)
- Configuración de servidor
- Instalación de dependencias
- Configuración de base de datos
- Despliegue con Gunicorn y Nginx
- Configuración de SSL
- Backup y mantenimiento

## 🛠️ Scripts Disponibles

### Scripts de Inicialización
- `init_payment_db.py` - Base de datos completa con pagos
- `init_admin.py` - Crear usuario administrador
- `init_sample_data.py` - Cargar datos de ejemplo

### Scripts de Mantenimiento
- `update_payment_schema.py` - Actualizar esquema de pagos
- `update_db_schema.py` - Actualizar esquema general
- `check_db.py` - Verificar integridad de BD
- `check_db_path.py` - Verificar rutas de BD

## 🔧 Configuración

### Archivos de Configuración
- `config.example.py` - Configuración completa de ejemplo
- `env.example` - Variables de entorno de ejemplo
- `config.py` - Configuración actual (no subir al repositorio)

### Variables de Entorno Importantes
- `SECRET_KEY` - Clave secreta de la aplicación
- `DATABASE_URL` - URL de conexión a base de datos
- `TRANSBANK_*` - Configuración de Transbank
- `FLASK_ENV` - Entorno de Flask

### Dependencias Principales
- `transbank-sdk>=1.0.0` - SDK oficial de Transbank (instalado via pip)
- `Flask==3.0.2` - Framework web
- `Flask-SQLAlchemy==3.1.1` - ORM para base de datos
- `Flask-Login==0.6.3` - Autenticación de usuarios

## 🚀 Beneficios de la Reorganización

### 1. **Mejor Organización**
- Estructura clara y lógica
- Separación de responsabilidades
- Fácil navegación del proyecto

### 2. **Documentación Profesional**
- Documentación completa y estructurada
- Guías paso a paso
- Ejemplos y casos de uso

### 3. **Mantenimiento Simplificado**
- Scripts organizados por función
- Configuración centralizada
- Procesos automatizados

### 4. **Escalabilidad**
- Estructura preparada para crecimiento
- Separación de entornos (dev/prod)
- Configuración flexible

### 5. **Colaboración Mejorada**
- Documentación clara para nuevos desarrolladores
- Estructura estándar de proyecto
- Guías de contribución

### 6. **Proyecto Más Limpio**
- Eliminación de código fuente duplicado
- Dependencias gestionadas via pip
- Estructura más profesional

## 📋 Próximos Pasos

### 1. **Testing**
- Implementar tests unitarios en `tests/`
- Tests de integración
- Tests de API

### 2. **CI/CD**
- Configurar GitHub Actions
- Automatizar despliegue
- Tests automáticos

### 3. **Monitoreo**
- Implementar logging avanzado
- Métricas de aplicación
- Alertas automáticas

### 4. **Seguridad**
- Auditoría de seguridad
- Implementar rate limiting
- Validación avanzada de inputs

---

**Versión de la estructura:** 1.1.0  
**Fecha de reorganización:** Junio 2025  
**Estado:** ✅ Completado  
**Última actualización:** Eliminación de carpeta transbank-sdk-python-master 