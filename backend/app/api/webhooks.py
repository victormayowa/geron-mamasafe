"""
WhatsApp/SMS Webhook endpoints
Handles incoming messages from Twilio
"""

from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import datetime
import logging

from app.core.database import get_db
from app.models.models import Mother, Child, Message, Consultation, RiskLevel
from app.schemas.schemas import WhatsAppMessage, SMSMessage
from app.services.ai_consultation import AIConsultationService
from app.services.twilio_service import TwilioMessageService
from app.services.danger_signs_db import DangerSignsDatabase

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/whatsapp")
async def handle_whatsapp_message(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle incoming WhatsApp messages"""
    
    # Parse form data from Twilio
    form_data = await request.form()
    
    from_number = form_data.get("From")
    to_number = form_data.get("To")
    body = form_data.get("Body", "")
    message_sid = form_data.get("MessageSid")
    profile_name = form_data.get("ProfileName")
    
    if not from_number or not body:
        return {"status": "error", "message": "Missing required fields"}
    
    logger.info(f"Received WhatsApp message from {from_number}: {body[:50]}...")
    
    # Log incoming message
    await log_incoming_message(db, from_number, body, "whatsapp", message_sid)
    
    # Find or identify mother
    mother = await find_mother_by_phone(db, from_number)
    
    if not mother:
        # New user - send registration message
        twilio = TwilioMessageService()
        await twilio.send_whatsapp_message(
            from_number,
            "Welcome to Geron Mamasafe! 🌸\n\nTo get started, please visit your nearest health center to register.\n\nIf you're already registered, please provide your phone number."
        )
        return {"status": "success", "message": "Registration prompt sent"}
    
    # Update last interaction
    mother.last_interaction = datetime.utcnow()
    await db.commit()
    
    # Check for common commands
    response = await process_command(body.strip().lower(), mother)
    
    if response:
        twilio = TwilioMessageService()
        await twilio.send_whatsapp_message(from_number, response)
        return {"status": "success", "message": "Command response sent"}
    
    # Process with AI consultation
    consultation_service = AIConsultationService()
    
    # Get mother's profile context
    mother_profile = {
        "pregnancy_stage": mother.pregnancy_stage.value if mother.pregnancy_stage else None,
        "risk_level": mother.risk_level.value if mother.risk_level else None,
        "expected_due_date": mother.expected_due_date.isoformat() if mother.expected_due_date else None
    }
    
    # Get child profiles if any
    child_profiles = []
    if mother.children:
        for child in mother.children:
            if child.is_active:
                child_profiles.append({
                    "age_group": child.age_group.value if child.age_group else None,
                    "date_of_birth": child.date_of_birth.isoformat()
                })
    
    # Process query
    result = await consultation_service.process_query(
        body,
        mother_profile=mother_profile,
        child_profile=child_profiles[0] if child_profiles else None
    )
    
    # Log consultation
    consultation = Consultation(
        mother_id=mother.id,
        query=body,
        response=result["response"],
        category=result["category"],
        urgency_level=result["urgency_level"],
        ai_confidence=result["ai_confidence"],
        requires_follow_up=result["requires_follow_up"],
        escalated=result["escalated"]
    )
    db.add(consultation)
    
    # Send response
    twilio = TwilioMessageService()
    await twilio.send_whatsapp_message(from_number, result["response"])
    
    # If escalated, send alert to health provider
    if result["escalated"]:
        logger.warning(f"URGENT: Mother {mother.id} ({from_number}) needs immediate attention. Query: {body}")
        # Here you would send alert to health provider
        # For now, just log it
    
    await db.commit()
    
    return {"status": "success", "message": "Response sent"}


@router.post("/sms")
async def handle_sms_message(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle incoming SMS messages"""
    
    # Parse form data from Twilio
    form_data = await request.form()
    
    from_number = form_data.get("From")
    to_number = form_data.get("To")
    body = form_data.get("Body", "")
    message_sid = form_data.get("MessageSid")
    
    if not from_number or not body:
        return {"status": "error", "message": "Missing required fields"}
    
    logger.info(f"Received SMS from {from_number}: {body[:50]}...")
    
    # Log incoming message
    await log_incoming_message(db, from_number, body, "sms", message_sid)
    
    # Find mother
    mother = await find_mother_by_phone(db, from_number)
    
    if not mother:
        # New user
        twilio = TwilioMessageService()
        await twilio.send_sms(
            from_number,
            "Welcome to Geron Mamasafe! Visit your health center to register."
        )
        return {"status": "success"}
    
    # Update last interaction
    mother.last_interaction = datetime.utcnow()
    await db.commit()
    
    # Check commands
    response = await process_command(body.strip().lower(), mother)
    
    if response:
        twilio = TwilioMessageService()
        await twilio.send_sms(from_number, response)
        return {"status": "success"}
    
    # Process with AI
    consultation_service = AIConsultationService()
    
    mother_profile = {
        "pregnancy_stage": mother.pregnancy_stage.value if mother.pregnancy_stage else None,
        "risk_level": mother.risk_level.value if mother.risk_level else None
    }
    
    result = await consultation_service.process_query(body, mother_profile=mother_profile)
    
    # Log consultation
    consultation = Consultation(
        mother_id=mother.id,
        query=body,
        response=result["response"],
        category=result["category"],
        urgency_level=result["urgency_level"],
        ai_confidence=result["ai_confidence"],
        requires_follow_up=result["requires_follow_up"],
        escalated=result["escalated"]
    )
    db.add(consultation)
    
    # Send response
    twilio = TwilioMessageService()
    await twilio.send_sms(from_number, result["response"])
    
    await db.commit()
    
    return {"status": "success"}


@router.post("/status")
async def handle_status_callback(request: Request):
    """Handle message status callbacks"""
    form_data = await request.form()
    
    message_sid = form_data.get("MessageSid")
    status = form_data.get("MessageStatus")
    error_code = form_data.get("ErrorCode")
    error_message = form_data.get("ErrorMessage")
    
    logger.info(f"Message {message_sid} status: {status}")
    
    # Update message status in database
    # This would be implemented based on your message tracking needs
    
    return {"status": "success"}


async def process_command(command: str, mother: Mother) -> Optional[str]:
    """Process common commands"""
    
    if command in ["help", "menu", "options"]:
        return f"""Hello {mother.first_name}! 👋

Available commands:
• Just type your question about pregnancy or child health
• Type "danger signs" to see warning signs
• Type "appointment" for next appointment info
• Type "emergency" for emergency contacts
• Type "status" to see your pregnancy/child info

💚 We're here to help!"""
    
    elif command in ["danger signs", "danger", "warning"]:
        danger_signs = DangerSignsDatabase.get_maternal_danger_signs(mother.pregnancy_stage or "first_trimester")
        
        if danger_signs:
            signs_text = "\n".join([f"• {sign['sign_name']}" for sign in danger_signs[:5]])
            return f"""⚠️ Danger Signs to Watch:

{signs_text}

If you experience any of these, seek medical attention immediately.

Type any symptom for more details."""
        else:
            return "Visit your health center to learn about danger signs during pregnancy."
    
    elif command in ["emergency", "urgent", "help emergency"]:
        return """🚨 EMERGENCY GUIDANCE

Go to your nearest secondary or tertiary facility IMMEDIATELY if experiencing:
• Heavy bleeding
• Severe headache with vision changes
• Difficulty breathing
• Convulsions
• Severe abdominal pain
• Reduced baby movements

Don't wait! Seek care now!"""
    
    elif command in ["status", "my info", "my information"]:
        status_msg = f"""📋 Your Information:

Name: {mother.first_name} {mother.last_name}"""
        
        if mother.pregnancy_stage:
            status_msg += f"\nPregnancy Stage: {mother.pregnancy_stage.value.replace('_', ' ').title()}"
        
        if mother.expected_due_date:
            status_msg += f"\nExpected Due Date: {mother.expected_due_date.strftime('%B %d, %Y')}"
        
        if mother.risk_level:
            status_msg += f"\nRisk Level: {mother.risk_level.value.upper()}"
        
        status_msg += "\n\n💚 Keep attending your appointments!"
        
        return status_msg
    
    elif command in ["appointment", "next appointment"]:
        return "📅 Please contact your health center for appointment scheduling. Attend all scheduled antenatal appointments!"
    
    return None


async def find_mother_by_phone(db: AsyncSession, phone_number: str) -> Optional[Mother]:
    """Find mother by phone number (with or without whatsapp: prefix)"""
    
    # Remove whatsapp: prefix if present
    clean_number = phone_number.replace("whatsapp:", "")
    
    result = await db.execute(
        select(Mother).where(
            (Mother.phone_number == clean_number) |
            (Mother.whatsapp_number == clean_number) |
            (Mother.phone_number == phone_number) |
            (Mother.whatsapp_number == phone_number)
        )
    )
    
    return result.scalar_one_or_none()


async def log_incoming_message(
    db: AsyncSession,
    from_number: str,
    body: str,
    channel: str,
    message_sid: Optional[str] = None
):
    """Log incoming message"""
    # Try to find mother
    mother = await find_mother_by_phone(db, from_number)
    
    if mother:
        message = Message(
            mother_id=mother.id,
            message_type="inbound",
            content=body,
            direction="inbound",
            channel=channel,
            status="received",
            twilio_sid=message_sid
        )
        db.add(message)
