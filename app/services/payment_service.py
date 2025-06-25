"""
Servicio de pagos integrado con Transbank
"""

import json
import logging
from datetime import datetime
from typing import Dict, Optional, Tuple
from flask import current_app
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType
from transbank.error.transbank_error import TransbankError
from transbank.error.transaction_create_error import TransactionCreateError
from transbank.error.transaction_commit_error import TransactionCommitError
from app import db
from app.models import Reservation, Payment

logger = logging.getLogger(__name__)

class PaymentService:
    """Servicio para manejar pagos con Transbank"""
    
    def __init__(self):
        self.transaction = self._initialize_transbank()
    
    def _initialize_transbank(self) -> Transaction:
        """Inicializa la configuración de Transbank"""
        try:
            # Obtener configuración desde Flask config
            commerce_code = current_app.config.get('TRANSBANK_COMMERCE_CODE')
            api_key = current_app.config.get('TRANSBANK_API_KEY')
            environment = current_app.config.get('TRANSBANK_ENVIRONMENT', 'TEST')
            
            # Configurar tipo de integración
            if environment.upper() == 'LIVE':
                integration_type = IntegrationType.LIVE
            else:
                integration_type = IntegrationType.TEST
            
            # Crear opciones de Webpay
            options = WebpayOptions(commerce_code, api_key, integration_type)
            
            # Crear instancia de transacción
            return Transaction(options)
            
        except Exception as e:
            logger.error(f"Error inicializando Transbank: {e}")
            raise
    
    def create_payment(self, reservation: Reservation) -> Tuple[bool, str, Optional[Dict]]:
        """
        Crea una transacción de pago para una reserva
        
        Args:
            reservation: Objeto Reservation
            
        Returns:
            Tuple[bool, str, Optional[Dict]]: (éxito, mensaje, datos_transacción)
        """
        try:
            # Validar que la reserva esté pendiente de pago o fallida (para reintentar)
            if reservation.payment_status not in ['pending', 'failed']:
                return False, "La reserva ya no está pendiente de pago", None
            
            # Si es un reintento de pago fallido, eliminar pagos anteriores
            if reservation.payment_status == 'failed':
                existing_payments = Payment.query.filter_by(reservation_id=reservation.id).all()
                for payment in existing_payments:
                    db.session.delete(payment)
                db.session.commit()
                logger.info(f"Pagos anteriores eliminados para reintento de reserva {reservation.id}")
            
            # Generar orden de compra única
            buy_order = f"RES_{reservation.id}_{int(datetime.now().timestamp())}"
            session_id = f"session_{reservation.user_id}_{int(datetime.now().timestamp())}"
            
            # URL de retorno
            return_url = current_app.config.get('TRANSBANK_RETURN_URL')
            
            # Crear transacción en Transbank
            response = self.transaction.create(
                buy_order=buy_order,
                session_id=session_id,
                amount=reservation.total_price,
                return_url=return_url
            )
            
            # Crear registro de pago
            payment = Payment(
                reservation_id=reservation.id,
                amount=reservation.total_price,
                status='processing',
                token=response.get('token'),
                payment_method='webpay',
                transbank_response=json.dumps(response)
            )
            
            # Actualizar estado de la reserva
            reservation.payment_status = 'processing'
            reservation.payment_token = response.get('token')
            reservation.payment_amount = reservation.total_price
            
            # Guardar en base de datos
            db.session.add(payment)
            db.session.commit()
            
            logger.info(f"Pago creado exitosamente para reserva {reservation.id}")
            print('DEBUG response Transbank:', response)
            # Si no hay URL, usar una de prueba
            url_pago = response.get('url') or f"/payment/status/{reservation.id}"
            response['url'] = url_pago
            return True, "Transacción creada exitosamente", response
            
        except TransactionCreateError as e:
            logger.error(f"Error creando transacción: {e}")
            return False, f"Error creando transacción: {e.message}", None
        except Exception as e:
            logger.error(f"Error inesperado creando pago: {e}")
            db.session.rollback()
            return False, f"Error inesperado: {str(e)}", None
    
    def confirm_payment(self, token: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Confirma una transacción de pago
        
        Args:
            token: Token de la transacción de Transbank
            
        Returns:
            Tuple[bool, str, Optional[Dict]]: (éxito, mensaje, datos_transacción)
        """
        try:
            # Buscar pago por token
            payment = Payment.query.filter_by(token=token).first()
            if not payment:
                return False, "No se encontró el pago con el token proporcionado", None
            
            # Confirmar transacción en Transbank
            response = self.transaction.commit(token)
            
            # Actualizar pago
            payment.transbank_response = json.dumps(response)
            payment.completed_at = datetime.utcnow()
            
            # Verificar respuesta de Transbank
            if response.get('response_code') == 0:  # Pago exitoso
                payment.status = 'completed'
                payment.transbank_transaction_id = response.get('authorization_code')
                
                # Actualizar reserva
                reservation = payment.reservation_ref
                reservation.payment_status = 'completed'
                reservation.payment_date = datetime.utcnow()
                reservation.transbank_transaction_id = response.get('authorization_code')
                reservation.status = 'confirmed'  # Confirmar la reserva
                
                db.session.commit()
                
                logger.info(f"Pago confirmado exitosamente para reserva {reservation.id}")
                return True, "Pago confirmado exitosamente", response
            else:
                # Pago fallido
                payment.status = 'failed'
                payment.error_message = response.get('response_description', 'Error desconocido')
                
                # Actualizar reserva
                reservation = payment.reservation_ref
                reservation.payment_status = 'failed'
                
                db.session.commit()
                
                logger.warning(f"Pago fallido para reserva {reservation.id}: {response.get('response_description')}")
                return False, f"Pago fallido: {response.get('response_description')}", response
                
        except TransactionCommitError as e:
            logger.error(f"Error confirmando transacción: {e}")
            return False, f"Error confirmando transacción: {e.message}", None
        except Exception as e:
            logger.error(f"Error inesperado confirmando pago: {e}")
            db.session.rollback()
            return False, f"Error inesperado: {str(e)}", None
    
    def check_payment_status(self, token: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Consulta el estado de una transacción
        
        Args:
            token: Token de la transacción de Transbank
            
        Returns:
            Tuple[bool, str, Optional[Dict]]: (éxito, mensaje, datos_transacción)
        """
        try:
            response = self.transaction.status(token)
            return True, "Estado consultado exitosamente", response
            
        except Exception as e:
            logger.error(f"Error consultando estado de transacción: {e}")
            return False, f"Error consultando estado: {str(e)}", None
    
    def refund_payment(self, token: str, amount: float) -> Tuple[bool, str, Optional[Dict]]:
        """
        Reembolsa una transacción
        
        Args:
            token: Token de la transacción de Transbank
            amount: Monto a reembolsar
            
        Returns:
            Tuple[bool, str, Optional[Dict]]: (éxito, mensaje, datos_transacción)
        """
        try:
            # Buscar pago por token
            payment = Payment.query.filter_by(token=token).first()
            if not payment:
                return False, "No se encontró el pago con el token proporcionado", None
            
            # Procesar reembolso en Transbank
            response = self.transaction.refund(token, amount)
            
            # Actualizar pago
            payment.status = 'refunded'
            payment.transbank_response = json.dumps(response)
            payment.completed_at = datetime.utcnow()
            
            # Actualizar reserva
            reservation = payment.reservation_ref
            reservation.payment_status = 'refunded'
            
            db.session.commit()
            
            logger.info(f"Reembolso procesado exitosamente para reserva {reservation.id}")
            return True, "Reembolso procesado exitosamente", response
            
        except Exception as e:
            logger.error(f"Error procesando reembolso: {e}")
            db.session.rollback()
            return False, f"Error procesando reembolso: {str(e)}", None
    
    def get_payment_by_reservation(self, reservation_id: int) -> Optional[Payment]:
        """Obtiene el pago asociado a una reserva"""
        return Payment.query.filter_by(reservation_id=reservation_id).first()
    
    def get_payment_by_token(self, token: str) -> Optional[Payment]:
        """Obtiene el pago por token"""
        return Payment.query.filter_by(token=token).first() 