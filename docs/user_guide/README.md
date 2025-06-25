# 👥 Manual de Usuario - Sistema Salfa

## 📋 Índice

1. [Introducción](#-introducción)
2. [Primeros Pasos](#-primeros-pasos)
3. [Registro e Inicio de Sesión](#-registro-e-inicio-de-sesión)
4. [Explorar Vehículos y Maquinarias](#-explorar-vehículos-y-maquinarias)
5. [Crear Reservas](#-crear-reservas)
6. [Sistema de Pagos](#-sistema-de-pagos)
7. [Gestionar Mis Reservas](#-gestionar-mis-reservas)
8. [Notificaciones](#-notificaciones)
9. [Panel de Administración](#-panel-de-administración)
10. [Solución de Problemas](#-solución-de-problemas)

## 🎯 Introducción

El Sistema de Gestión de Vehículos y Maquinarias Salfa es una plataforma web que permite a los usuarios reservar vehículos y maquinarias pesadas de forma fácil y segura, con integración completa de pagos a través de Transbank.

### ¿Qué puedes hacer?

- 🚗 **Explorar** catálogo de vehículos y maquinarias
- 📅 **Reservar** equipos para fechas específicas
- 💳 **Pagar** de forma segura con Transbank
- 📊 **Gestionar** tus reservas y pagos
- 🔔 **Recibir** notificaciones en tiempo real

## 🚀 Primeros Pasos

### Requisitos del Sistema

- **Navegador web** moderno (Chrome, Firefox, Safari, Edge)
- **Conexión a internet** estable
- **JavaScript habilitado** en el navegador

### Acceso al Sistema

1. Abre tu navegador web
2. Ve a la URL del sistema: `http://127.0.0.1:5000`
3. Verás la página principal con el catálogo de vehículos

## 🔐 Registro e Inicio de Sesión

### Crear una Cuenta

1. **Haz clic** en "Iniciar Sesión" en la esquina superior derecha
2. **Haz clic** en "Registrarse" en la página de login
3. **Completa** el formulario con:
   - **Nombre de usuario** (único)
   - **Email** (válido)
   - **Contraseña** (mínimo 6 caracteres)
4. **Haz clic** en "Registrarse"
5. **Confirma** tu registro

### Iniciar Sesión

1. **Haz clic** en "Iniciar Sesión"
2. **Ingresa** tu nombre de usuario o email
3. **Ingresa** tu contraseña
4. **Haz clic** en "Iniciar Sesión"

### Cerrar Sesión

- **Haz clic** en tu nombre de usuario en la esquina superior derecha
- **Selecciona** "Cerrar Sesión"

## 🚗 Explorar Vehículos y Maquinarias

### Ver Catálogo de Vehículos

1. **Haz clic** en "Vehículos" en el menú principal
2. **Explora** las tarjetas de vehículos disponibles
3. **Cada tarjeta muestra:**
   - Imagen del vehículo
   - Nombre y modelo
   - Año de fabricación
   - Precio por día
   - Estado de disponibilidad

### Ver Catálogo de Maquinarias

1. **Haz clic** en "Maquinarias" en el menú principal
2. **Explora** las tarjetas de maquinarias disponibles
3. **Cada tarjeta muestra:**
   - Imagen de la maquinaria
   - Nombre y modelo
   - Especificaciones técnicas
   - Precio por día
   - Estado de disponibilidad

### Filtrar y Buscar

- **Usa** los filtros por categoría si están disponibles
- **Busca** por nombre o modelo en la barra de búsqueda
- **Ordena** por precio, año o disponibilidad

## 📅 Crear Reservas

### Reservar un Vehículo

1. **Navega** al catálogo de vehículos
2. **Selecciona** el vehículo que deseas reservar
3. **Haz clic** en "Reservar"
4. **Completa** el formulario de reserva:
   - **Fecha de inicio** (cuándo necesitas el vehículo)
   - **Fecha de fin** (cuándo lo devolverás)
5. **Revisa** el precio total calculado automáticamente
6. **Haz clic** en "Confirmar Reserva"

### Reservar una Maquinaria

1. **Navega** al catálogo de maquinarias
2. **Selecciona** la maquinaria que necesitas
3. **Haz clic** en "Reservar"
4. **Completa** el formulario de reserva:
   - **Fecha de inicio**
   - **Fecha de fin**
   - **Ubicación del proyecto** (obligatorio)
5. **Revisa** el precio total
6. **Haz clic** en "Confirmar Reserva"

### Validaciones Importantes

- ✅ **Fechas válidas**: La fecha de fin debe ser posterior a la de inicio
- ✅ **Disponibilidad**: El sistema verifica que no haya conflictos
- ✅ **Fechas futuras**: No puedes reservar para fechas pasadas
- ✅ **Duración mínima**: Algunos equipos tienen duración mínima

## 💳 Sistema de Pagos

### Proceso de Pago

1. **Después de confirmar** la reserva, serás redirigido al pago
2. **Verás** una página de redirección a Transbank
3. **Serás enviado** automáticamente a la página de pago de Transbank
4. **Completa** el formulario de pago con:
   - **Número de tarjeta**
   - **Fecha de vencimiento**
   - **CVV**
   - **RUT del titular**
   - **Clave de la tarjeta**
5. **Confirma** el pago
6. **Serás redirigido** de vuelta al sistema

### Credenciales de Prueba

Para pruebas, usa estas credenciales:

- **Tarjeta:** `4051 8856 0044 6623`
- **Fecha:** Cualquier fecha futura (ej: 12/29)
- **CVV:** Cualquier número de 3 dígitos (ej: 123)
- **RUT:** `11.111.111-1`
- **Clave:** `123`

### Estados de Pago

- 🔄 **Pendiente**: Reserva creada, pendiente de pago
- ⏳ **Procesando**: Pago en curso
- ✅ **Completado**: Pago exitoso, reserva confirmada
- ❌ **Fallido**: Pago rechazado, puedes reintentar
- 💰 **Reembolsado**: Pago devuelto por administrador

### Reintentar Pago Fallido

Si tu pago falla:

1. **Ve** a "Mis Reservas"
2. **Busca** la reserva con estado "Fallido"
3. **Haz clic** en "Reintentar Pago"
4. **Sigue** el proceso de pago nuevamente

## 📊 Gestionar Mis Reservas

### Ver Mis Reservas

1. **Haz clic** en "Mis Reservas" en el menú principal
2. **Verás** todas tus reservas ordenadas por fecha
3. **Cada reserva muestra:**
   - Imagen del vehículo/maquinaria
   - Fechas de inicio y fin
   - Precio total
   - Estado de la reserva
   - Estado del pago

### Estados de Reserva

- 🔄 **Pendiente**: Esperando confirmación del administrador
- ✅ **Confirmada**: Reserva aprobada y lista
- 🚗 **En Curso**: Equipo en uso
- 🏁 **Completada**: Uso finalizado
- ❌ **Cancelada**: Reserva cancelada

### Acciones Disponibles

- **Ver detalles** de la reserva
- **Proceder al pago** (si está pendiente)
- **Reintentar pago** (si falló)
- **Ver estado de pago** (si está completado)

## 🔔 Notificaciones

### Ver Notificaciones

1. **Haz clic** en el ícono de campana en la barra superior
2. **Verás** todas tus notificaciones no leídas
3. **Haz clic** en "Ver Todas" para ver el historial completo

### Tipos de Notificaciones

- ℹ️ **Informativa**: Información general
- ✅ **Éxito**: Confirmaciones y logros
- ⚠️ **Advertencia**: Avisos importantes
- ❌ **Error**: Problemas o errores

### Gestionar Notificaciones

- **Haz clic** en una notificación para marcarla como leída
- **Haz clic** en "Marcar todas como leídas" para limpiar todas
- **Las notificaciones** se crean automáticamente para:
  - Confirmación de reservas
  - Inicio de uso de equipos
  - Finalización de reservas
  - Cancelaciones
  - Problemas con pagos

## 👨‍💼 Panel de Administración

### Acceso al Panel

1. **Inicia sesión** con credenciales de administrador
2. **Haz clic** en "Administración" en el menú
3. **Verás** el dashboard principal

### Gestión de Usuarios

1. **Haz clic** en "Usuarios" en el panel
2. **Verás** lista de todos los usuarios registrados
3. **Acciones disponibles:**
   - Ver detalles del usuario
   - Editar información
   - Cambiar rol (usuario/admin)
   - Desactivar cuenta

### Gestión de Vehículos y Maquinarias

1. **Haz clic** en "Vehículos" o "Maquinarias"
2. **Acciones disponibles:**
   - **Agregar** nuevo equipo
   - **Editar** información existente
   - **Eliminar** equipos
   - **Cambiar** estado de disponibilidad

### Gestión de Reservas

1. **Haz clic** en "Reservas" en el panel
2. **Verás** todas las reservas del sistema
3. **Acciones disponibles:**
   - **Confirmar** reservas pendientes
   - **Iniciar** uso de equipos
   - **Completar** reservas
   - **Cancelar** reservas con motivo

### Gestión de Pagos

1. **Haz clic** en "Pagos" en el panel
2. **Verás** todos los pagos del sistema
3. **Acciones disponibles:**
   - **Ver detalles** de cada pago
   - **Procesar reembolsos** para pagos completados
   - **Consultar estado** con Transbank

## 🛠️ Solución de Problemas

### Problemas Comunes

#### No puedo iniciar sesión
- ✅ Verifica que tu usuario y contraseña sean correctos
- ✅ Asegúrate de que la cuenta no esté bloqueada
- ✅ Contacta al administrador si olvidaste tu contraseña

#### No puedo crear una reserva
- ✅ Verifica que las fechas sean válidas
- ✅ Asegúrate de que el equipo esté disponible
- ✅ Revisa que no haya conflictos con otras reservas

#### El pago no funciona
- ✅ Verifica que tu tarjeta tenga fondos suficientes
- ✅ Asegúrate de que los datos de la tarjeta sean correctos
- ✅ Revisa que tu banco permita transacciones online
- ✅ Usa las credenciales de prueba para verificar

#### No recibo notificaciones
- ✅ Verifica que tu navegador permita notificaciones
- ✅ Revisa la carpeta de spam en tu email
- ✅ Contacta al administrador si el problema persiste

### Contacto de Soporte

Si tienes problemas que no puedes resolver:

- 📧 **Email**: [soporte@salfa.cl]
- 📱 **WhatsApp**: [+56 9 XXXX XXXX]
- 🕒 **Horario**: Lunes a Viernes 9:00 - 18:00

### Información para Reportes

Cuando reportes un problema, incluye:

1. **Descripción** detallada del problema
2. **Pasos** para reproducirlo
3. **Navegador** y versión que usas
4. **Sistema operativo**
5. **Captura de pantalla** si es posible
6. **Tu nombre de usuario** (sin contraseña)

## 📱 Consejos de Uso

### Para una Mejor Experiencia

- 📱 **Usa un navegador moderno** para mejor compatibilidad
- 🔄 **Actualiza la página** si algo no funciona correctamente
- 💾 **Guarda tus credenciales** en un lugar seguro
- 📅 **Planifica con anticipación** para mejores disponibilidades
- 💳 **Ten tu tarjeta lista** antes de iniciar el pago

### Seguridad

- 🔒 **No compartas** tus credenciales de acceso
- 🚪 **Cierra sesión** cuando termines de usar el sistema
- 💳 **Usa tarjetas seguras** para los pagos
- 📧 **Verifica** que estés en el sitio correcto

---

**Versión del manual:** 1.0.0  
**Última actualización:** Junio 2025  
**Para soporte técnico:** [soporte@salfa.cl] 