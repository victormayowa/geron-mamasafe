"""
Twilio WhatsApp and SMS Service
Handles sending and receiving messages via WhatsApp and SMS
"""

import logging
from typing import Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from app.core.config import settings

logger = logging.getLogger(__name__)


class TwilioMessageService:
    """Service for sending WhatsApp and SMS messages via Twilio"""

    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.whatsapp_number = settings.TWILIO_WHATSAPP_NUMBER
        self.phone_number = settings.TWILIO_PHONE_NUMBER

    async def send_whatsapp_message(self, to_number: str, message: str) -> dict:
        """
        Send a WhatsApp message
        
        Args:
            to_number: Recipient's WhatsApp number (format: whatsapp:+234...)
            message: Message text
            
        Returns:
            Message SID and status
        """
        try:
            # Ensure number has whatsapp: prefix
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'
            
            message_obj = self.client.messages.create(
                body=message,
                from_=self.whatsapp_number,
                to=to_number
            )
            
            logger.info(f"WhatsApp message sent successfully: {message_obj.sid}")
            return {
                "success": True,
                "message_sid": message_obj.sid,
                "status": message_obj.status,
                "channel": "whatsapp"
            }
            
        except TwilioRestException as e:
            logger.error(f"Failed to send WhatsApp message: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "channel": "whatsapp"
            }
        except Exception as e:
            logger.error(f"Unexpected error sending WhatsApp message: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "channel": "whatsapp"
            }

    async def send_sms(self, to_number: str, message: str) -> dict:
        """
        Send an SMS message
        
        Args:
            to_number: Recipient's phone number (format: +234...)
            message: Message text
            
        Returns:
            Message SID and status
        """
        try:
            message_obj = self.client.messages.create(
                body=message,
                from_=self.phone_number,
                to=to_number
            )
            
            logger.info(f"SMS message sent successfully: {message_obj.sid}")
            return {
                "success": True,
                "message_sid": message_obj.sid,
                "status": message_obj.status,
                "channel": "sms"
            }
            
        except TwilioRestException as e:
            logger.error(f"Failed to send SMS: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "channel": "sms"
            }
        except Exception as e:
            logger.error(f"Unexpected error sending SMS: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "channel": "sms"
            }

    async def send_message(self, to_number: str, message: str, channel: str = "whatsapp") -> dict:
        """
        Send a message via specified channel
        
        Args:
            to_number: Recipient's number
            message: Message text
            channel: 'whatsapp' or 'sms'
            
        Returns:
            Message result
        """
        if channel == "whatsapp":
            return await self.send_whatsapp_message(to_number, message)
        elif channel == "sms":
            return await self.send_sms(to_number, message)
        else:
            return {
                "success": False,
                "error": f"Unsupported channel: {channel}",
                "channel": channel
            }

    async def send_daily_education_message(self, mother_phone: str, content: str, channel: str = "whatsapp") -> dict:
        """
        Send daily health education message
        
        Args:
            mother_phone: Mother's phone number
            content: Educational message content
            channel: Message channel
            
        Returns:
            Message result
        """
        # Add greeting and formatting
        formatted_message = f"""🌅 *Geron Mamasafe - Daily Health Tip*

{content}

💚 _Stay informed, stay healthy!_
_Reply with any question for personalized advice_"""

        return await self.send_message(mother_phone, formatted_message, channel)

    async def send_alert_message(self, mother_phone: str, alert_title: str, alert_description: str, severity: str, channel: str = "whatsapp") -> dict:
        """
        Send alert message for danger signs or important notifications
        
        Args:
            mother_phone: Mother's phone number
            alert_title: Alert title
            alert_description: Alert description
            severity: Alert severity level
            channel: Message channel
            
        Returns:
            Message result
        """
        if severity == "critical":
            emoji = "🚨"
            urgency = "URGENT"
        elif severity == "high":
            emoji = "⚠️"
            urgency = "HIGH PRIORITY"
        elif severity == "medium":
            emoji = "⚡"
            urgency = "IMPORTANT"
        else:
            emoji = "ℹ️"
            urgency = "NOTICE"

        formatted_message = f"""{emoji} *{urgency} - {alert_title}*

{alert_description}

🏥 *Please seek medical attention as advised.*
_Contact your healthcare provider if you have questions._"""

        return await self.send_message(mother_phone, formatted_message, channel)

    async def send_appointment_reminder(self, mother_phone: str, appointment_details: str, channel: str = "whatsapp") -> dict:
        """
        Send appointment reminder message
        
        Args:
            mother_phone: Mother's phone number
            appointment_details: Appointment details
            channel: Message channel
            
        Returns:
            Message result
        """
        formatted_message = f"""📅 *Appointment Reminder*

{appointment_details}

⏰ _Don't forget to attend your appointment!_
_Contact your health center if you need to reschedule._"""

        return await self.send_message(mother_phone, formatted_message, channel)

    def validate_whatsapp_number(self, phone_number: str) -> bool:
        """
        Validate if a phone number can receive WhatsApp messages
        
        Args:
            phone_number: Phone number to validate
            
        Returns:
            True if valid
        """
        try:
            # Add whatsapp: prefix for validation
            if not phone_number.startswith('whatsapp:'):
                phone_number = f'whatsapp:{phone_number}'
            
            # Fetch number info from Twilio
            self.client.lookups.v2.phone_numbers(phone_number).fetch()
            return True
        except Exception as e:
            logger.error(f"Failed to validate WhatsApp number: {str(e)}")
            return False

    def get_message_status(self, message_sid: str) -> dict:
        """
        Get the status of a sent message
        
        Args:
            message_sid: Message SID
            
        Returns:
            Message status
        """
        try:
            message = self.client.messages(message_sid).fetch()
            return {
                "sid": message.sid,
                "status": message.status,
                "error_code": message.error_code,
                "error_message": message.error_message
            }
        except Exception as e:
            logger.error(f"Failed to get message status: {str(e)}")
            return {
                "sid": message_sid,
                "status": "unknown",
                "error": str(e)
            }
