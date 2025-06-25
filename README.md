# 🚗 Sistema de Gestión de Vehículos y Maquinarias - Salfa

## 📋 Descripción

Sistema web completo para la gestión de reservas de vehículos y maquinarias con integración de pagos Transbank. Desarrollado en Flask con funcionalidades de administración, reservas, pagos y notificaciones.

## ✨ Características Principales

- 🔐 **Autenticación de usuarios** con roles (admin/usuario)
- 🚗 **Gestión de vehículos y maquinarias** con imágenes
- 📅 **Sistema de reservas** con validación de fechas
- 💳 **Integración completa con Transbank** para pagos
- 🔄 **Reintentos de pago** para transacciones fallidas
- 📊 **Panel de administración** completo
- 🔔 **Sistema de notificaciones** en tiempo real
- 📱 **Interfaz responsive** con Bootstrap

## 🏗️ Arquitectura del Proyecto

```
Integracion/
├── app/                    # Aplicación principal Flask
│   ├── auth/              # Autenticación y autorización
│   ├── main/              # Rutas principales
│   ├── services/          # Servicios de negocio
│   ├── static/            # Archivos estáticos (CSS, JS, imágenes)
│   ├── templates/         # Templates HTML
│   └── utils/             # Utilidades (conversión de monedas)
├── docs/                  # Documentación
│   ├── api/              # Documentación de API
│   ├── deployment/       # Guías de despliegue
│   └── user_guide/       # Manual de usuario
├── scripts/              # Scripts de inicialización y mantenimiento
├── tests/                # Tests unitarios y de integración
├── transbank-sdk-python-master/  # SDK de Transbank
└── venv/                 # Entorno virtual Python
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8+
- pip
- SQLite (incluido con Python)

### Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd Integracion
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   # Copiar y editar config.py con tus credenciales
   cp config.py.example config.py
   ```

5. **Inicializar base de datos**
   ```bash
   python scripts/init_payment_db.py
   ```

6. **Ejecutar la aplicación**
   ```bash
   python run.py
   ```

## 🔧 Configuración

### Variables de Entorno

Edita `config.py` con tus configuraciones:

```python
# Configuración de Transbank (ambiente de prueba)
TRANSBANK_COMMERCE_CODE = "597055555532"
TRANSBANK_API_KEY = "0208f0a6fa6a6a1a1a1a1a1a1a1a1a1a"
TRANSBANK_ENVIRONMENT = "TEST"
TRANSBANK_RETURN_URL = "http://127.0.0.1:5000/payment/return"

# Configuración de la aplicación
SECRET_KEY = "tu-clave-secreta-aqui"
DATABASE_URL = "sqlite:///instance/database.db"
```

### Credenciales de Prueba Transbank

- **Tarjeta:** `4051 8856 0044 6623`
- **Fecha:** Cualquier fecha futura
- **CVV:** Cualquier número de 3 dígitos
- **RUT:** `11.111.111-1`
- **Clave:** `123`

## 📖 Uso

### Usuarios

1. **Registro/Login** en `/auth/register` o `/auth/login`
2. **Explorar vehículos/maquinarias** en `/vehiculos` o `/maquinaria`
3. **Crear reserva** seleccionando fechas y confirmando
4. **Proceder al pago** con Transbank
5. **Ver estado** en `/mis_reservas`

### Administradores

1. **Login** con credenciales de administrador
2. **Panel de administración** en `/admin`
3. **Gestionar usuarios, vehículos, reservas y pagos**
4. **Confirmar/cancelar reservas**
5. **Procesar reembolsos**

## 🔄 Flujo de Pagos

1. **Usuario crea reserva** → Estado: `pending`
2. **Usuario procede al pago** → Estado: `processing`
3. **Redirección a Transbank** → Formulario de pago
4. **Usuario completa pago** → Retorno a aplicación
5. **Confirmación automática** → Estado: `completed` o `failed`
6. **Reintento disponible** si falla → Nuevo intento de pago

## 📚 Documentación

- **[Manual de Usuario](docs/user_guide/README.md)** - Guía completa para usuarios
- **[Documentación de API](docs/api/README.md)** - Endpoints y servicios
- **[Guía de Despliegue](docs/deployment/README.md)** - Instrucciones para producción
- **[Análisis de Requisitos](docs/Integración%20de%20Plataformas%20Caso%20Salfa%201.5%20Final[1]%20-%20copia.docx)** - Documento original

## 🛠️ Scripts Disponibles

- `scripts/init_payment_db.py` - Inicializar base de datos con pagos
- `scripts/init_admin.py` - Crear usuario administrador
- `scripts/init_sample_data.py` - Cargar datos de ejemplo
- `scripts/update_payment_schema.py` - Actualizar esquema de pagos

## 🧪 Testing

```bash
# Ejecutar tests
python -m pytest tests/

# Tests específicos
python -m pytest tests/test_payments.py
python -m pytest tests/test_reservations.py
```

## 🚀 Despliegue en Producción

Ver [Guía de Despliegue](docs/deployment/README.md) para instrucciones detalladas.

### Consideraciones de Producción

- ✅ Usar HTTPS
- ✅ Configurar credenciales reales de Transbank
- ✅ Usar servidor WSGI (Gunicorn/uWSGI)
- ✅ Configurar base de datos PostgreSQL/MySQL
- ✅ Implementar logging y monitoreo
- ✅ Configurar backup automático

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👥 Autores

- **Matías** - *Desarrollo inicial* - [TuUsuario]

## 🙏 Agradecimientos

- **Transbank** por el SDK de pagos
- **Flask** por el framework web
- **Bootstrap** por el diseño responsive

## 📞 Soporte

Para soporte técnico o preguntas:
- 📧 Email: [tu-email@ejemplo.com]
- 📱 WhatsApp: [+56 9 XXXX XXXX]
- 🐛 Issues: [URL del repositorio]/issues

---

**Versión:** 1.0.0  
**Última actualización:** Junio 2025  
**Estado:** ✅ Producción Ready 