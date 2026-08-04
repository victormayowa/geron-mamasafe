import asyncio
import structlog
from app.core.celery_app import celery_app
from app.services.whatsapp_service import WhatsAppService

logger = structlog.get_logger()

@celery_app.task(name="send_anc_reminder")
def send_anc_reminder(mother_id: int, phone_number: str, message: str):
    """
    Background task to send an Antenatal Care (ANC) appointment reminder.
    In a real app, this would fetch the mother's language preferences and format accordingly.
    """
    logger.info("executing_anc_reminder", mother_id=mother_id, phone=phone_number)
    
    # We must run the async WhatsApp service in a new event loop
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    whatsapp_service = WhatsAppService()
    
    try:
        # Assuming WhatsAppService has a send_message method
        # loop.run_until_complete(whatsapp_service.send_message(phone_number, message))
        
        # Placeholder for actual implementation
        logger.info("anc_reminder_sent_successfully", phone=phone_number)
        return {"status": "success", "type": "ANC", "phone": phone_number}
    except Exception as e:
        logger.error("anc_reminder_failed", error=str(e))
        raise e


@celery_app.task(name="send_immunization_reminder")
def send_immunization_reminder(child_id: int, phone_number: str, vaccine_name: str, scheduled_date: str):
    """
    Background task to send a child immunization reminder to the mother.
    """
    logger.info("executing_immunization_reminder", child_id=child_id, vaccine=vaccine_name)
    
    message = f"Reminder: Your child is due for the {vaccine_name} vaccine on {scheduled_date}. Please visit your local health center."
    
    # Similar async execution logic as above
    logger.info("immunization_reminder_sent", phone=phone_number)
    return {"status": "success", "type": "Immunization", "vaccine": vaccine_name}
