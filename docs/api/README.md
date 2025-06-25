# 📚 Documentación de API - Sistema Salfa

## 📋 Descripción General

Esta documentación describe todos los endpoints y servicios disponibles en el Sistema de Gestión de Vehículos y Maquinarias Salfa.

## 🔐 Autenticación

El sistema utiliza **Flask-Login** para la autenticación. La mayoría de endpoints requieren autenticación excepto los públicos.

### Endpoints Públicos
- `GET /` - Página principal
- `GET /auth/login` - Formulario de login
- `POST /auth/login` - Procesar login
- `GET /auth/register` - Formulario de registro
- `POST /auth/register` - Procesar registro
- `GET /auth/logout` - Cerrar sesión

## 🚗 Gestión de Vehículos

### Listar Vehículos
```
GET /vehiculos
```
**Descripción:** Muestra el catálogo de vehículos disponibles  
**Acceso:** Público  
**Respuesta:** Template HTML con lista de vehículos

### Agregar Vehículo
```
GET /vehiculos/add
POST /vehiculos/add
```
**Descripción:** Formulario para agregar nuevo vehículo  
**Acceso:** Solo administradores  
**Parámetros POST:**
- `name` (string) - Nombre del vehículo
- `model` (string) - Modelo
- `year` (integer) - Año
- `fuel_efficiency` (float) - Eficiencia de combustible
- `price_per_day` (float) - Precio por día
- `category` (string) - Categoría ('vehiculo' o 'maquinaria')
- `description` (text) - Descripción
- `image_url` (string) - Nombre del archivo de imagen

### Editar Vehículo
```
GET /vehiculos/edit/<id>
POST /vehiculos/edit/<id>
```
**Descripción:** Editar información de vehículo existente  
**Acceso:** Solo administradores  
**Parámetros:** Mismos que agregar vehículo

### Eliminar Vehículo
```
POST /vehiculos/delete/<id>
```
**Descripción:** Eliminar vehículo del sistema  
**Acceso:** Solo administradores

### Reservar Vehículo
```
POST /vehiculos/<vehicle_id>/reservar
```
**Descripción:** Crear reserva para un vehículo  
**Acceso:** Usuarios autenticados  
**Parámetros:**
- `start_date` (date) - Fecha de inicio (YYYY-MM-DD)
- `end_date` (date) - Fecha de fin (YYYY-MM-DD)

## 🏗️ Gestión de Maquinarias

### Listar Maquinarias
```
GET /maquinaria
```
**Descripción:** Muestra el catálogo de maquinarias disponibles  
**Acceso:** Público

### Agregar Maquinaria
```
GET /maquinaria/add
POST /maquinaria/add
```
**Descripción:** Formulario para agregar nueva maquinaria  
**Acceso:** Solo administradores  
**Parámetros:** Mismos que vehículos + `project_location`

### Editar Maquinaria
```
GET /maquinaria/edit/<id>
POST /maquinaria/edit/<id>
```
**Descripción:** Editar información de maquinaria existente  
**Acceso:** Solo administradores

### Eliminar Maquinaria
```
POST /maquinaria/delete/<id>
```
**Descripción:** Eliminar maquinaria del sistema  
**Acceso:** Solo administradores

### Reservar Maquinaria
```
POST /maquinaria/<vehicle_id>/reservar
```
**Descripción:** Crear reserva para una maquinaria  
**Acceso:** Usuarios autenticados  
**Parámetros:**
- `start_date` (date) - Fecha de inicio
- `end_date` (date) - Fecha de fin
- `project_location` (string) - Ubicación del proyecto

## 📅 Gestión de Reservas

### Mis Reservas
```
GET /mis_reservas
```
**Descripción:** Lista las reservas del usuario actual  
**Acceso:** Usuarios autenticados

### Administración de Reservas
```
GET /admin/reservas
```
**Descripción:** Panel de administración de todas las reservas  
**Acceso:** Solo administradores

### Confirmar Reserva
```
POST /admin/reservas/<reservation_id>/confirmar
```
**Descripción:** Confirmar una reserva pendiente  
**Acceso:** Solo administradores

### Iniciar Reserva
```
POST /admin/reservas/<reservation_id>/iniciar
```
**Descripción:** Marcar reserva como iniciada  
**Acceso:** Solo administradores

### Completar Reserva
```
POST /admin/reservas/<reservation_id>/completar
```
**Descripción:** Marcar reserva como completada  
**Acceso:** Solo administradores

### Cancelar Reserva
```
GET /admin/reservas/<reservation_id>/cancelar
POST /admin/reservas/<reservation_id>/cancelar
```
**Descripción:** Cancelar una reserva  
**Acceso:** Solo administradores  
**Parámetros POST:**
- `motivo` (text) - Motivo de la cancelación

## 💳 Sistema de Pagos

### Crear Pago
```
GET /payment/create/<reservation_id>
```
**Descripción:** Inicia el proceso de pago para una reserva  
**Acceso:** Usuarios autenticados (propietario de la reserva)  
**Flujo:**
1. Valida que la reserva esté pendiente o fallida
2. Crea transacción en Transbank
3. Redirige a formulario de pago

### Retorno de Pago
```
GET /payment/return
```
**Descripción:** URL de retorno después del pago en Transbank  
**Acceso:** Público  
**Parámetros:**
- `token_ws` (string) - Token de la transacción

### Estado de Pago
```
GET /payment/status/<reservation_id>
```
**Descripción:** Consulta el estado de pago de una reserva  
**Acceso:** Usuarios autenticados (propietario de la reserva)

### Administración de Pagos
```
GET /admin/payments
```
**Descripción:** Panel de administración de todos los pagos  
**Acceso:** Solo administradores

### Reembolso
```
POST /admin/payments/<payment_id>/refund
```
**Descripción:** Procesa un reembolso  
**Acceso:** Solo administradores

## 🔔 Sistema de Notificaciones

### Listar Notificaciones
```
GET /notificaciones
```
**Descripción:** Lista las notificaciones del usuario actual  
**Acceso:** Usuarios autenticados

### Marcar como Leída
```
GET /notificaciones/<notification_id>/marcar-leida
```
**Descripción:** Marca una notificación como leída  
**Acceso:** Usuarios autenticados (propietario de la notificación)

### Marcar Todas como Leídas
```
GET /notificaciones/marcar-todas-leidas
```
**Descripción:** Marca todas las notificaciones como leídas  
**Acceso:** Usuarios autenticados

## 👥 Gestión de Usuarios

### Administración de Usuarios
```
GET /admin/usuarios
```
**Descripción:** Panel de administración de usuarios  
**Acceso:** Solo administradores

### Panel de Administración
```
GET /admin
```
**Descripción:** Dashboard principal de administración  
**Acceso:** Solo administradores

## 🏗️ Estructura de Datos

### Modelo User
```python
{
    "id": integer,
    "username": string,
    "email": string,
    "is_admin": boolean,
    "created_at": datetime
}
```

### Modelo Vehicle
```python
{
    "id": integer,
    "name": string,
    "model": string,
    "year": integer,
    "fuel_efficiency": float,
    "price_per_day": float,
    "category": string,
    "description": text,
    "image_url": string,
    "available": boolean,
    "created_at": datetime
}
```

### Modelo Reservation
```python
{
    "id": integer,
    "user_id": integer,
    "vehicle_id": integer,
    "start_date": datetime,
    "end_date": datetime,
    "total_price": float,
    "status": string,
    "payment_status": string,
    "payment_token": string,
    "payment_amount": float,
    "payment_date": datetime,
    "transbank_transaction_id": string,
    "created_at": datetime
}
```

### Modelo Payment
```python
{
    "id": integer,
    "reservation_id": integer,
    "amount": float,
    "status": string,
    "token": string,
    "transbank_transaction_id": string,
    "payment_method": string,
    "created_at": datetime,
    "completed_at": datetime,
    "error_message": text,
    "transbank_response": text
}
```

### Modelo Notification
```python
{
    "id": integer,
    "user_id": integer,
    "title": string,
    "message": text,
    "type": string,
    "read": boolean,
    "created_at": datetime
}
```

## 🔄 Estados del Sistema

### Estados de Reserva
- `pending` - Pendiente de confirmación
- `confirmed` - Confirmada
- `in_progress` - En curso
- `completed` - Completada
- `cancelled` - Cancelada

### Estados de Pago
- `pending` - Pendiente de pago
- `processing` - Procesando pago
- `completed` - Pago completado
- `failed` - Pago fallido
- `refunded` - Reembolsado

### Tipos de Notificación
- `info` - Informativa
- `success` - Éxito
- `warning` - Advertencia
- `error` - Error

## 🛠️ Servicios

### PaymentService
Clase principal para manejo de pagos con Transbank.

**Métodos:**
- `create_payment(reservation)` - Crear transacción de pago
- `confirm_payment(token)` - Confirmar transacción
- `check_payment_status(token)` - Consultar estado
- `refund_payment(token, amount)` - Procesar reembolso

### Utilidades de Moneda
- `convert_to_uf(amount)` - Convertir a UF
- `convert_to_usd(amount)` - Convertir a USD
- `format_currency(amount, currency)` - Formatear moneda

## 🔒 Seguridad

### Validaciones
- Autenticación requerida para endpoints privados
- Verificación de propiedad de recursos
- Validación de roles de administrador
- Sanitización de inputs

### Protección CSRF
- Tokens CSRF en formularios
- Validación de origen de requests

### Manejo de Errores
- Páginas de error personalizadas
- Logging de errores
- Mensajes de error amigables

## 📊 Respuestas HTTP

### Códigos de Estado
- `200` - OK
- `302` - Redirect
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

### Formatos de Respuesta
- **HTML:** Templates renderizados
- **JSON:** Para APIs (futuro)
- **Redirect:** Para formularios

## 🔧 Configuración

### Variables de Entorno
```python
# Transbank
TRANSBANK_COMMERCE_CODE = "597055555532"
TRANSBANK_API_KEY = "0208f0a6fa6a6a1a1a1a1a1a1a1a1a1a"
TRANSBANK_ENVIRONMENT = "TEST"
TRANSBANK_RETURN_URL = "http://127.0.0.1:5000/payment/return"

# Aplicación
SECRET_KEY = "tu-clave-secreta"
DATABASE_URL = "sqlite:///instance/database.db"
```

## 🧪 Testing

### Endpoints de Prueba
- `/payment/create/<id>` - Crear pago de prueba
- `/payment/return` - Simular retorno de pago

### Datos de Prueba
- Usuario: `usuario` / `usuario123`
- Admin: `admin` / `admin123`
- Tarjeta Transbank: `4051 8856 0044 6623`

---

**Versión de la API:** 1.0.0  
**Última actualización:** Junio 2025 