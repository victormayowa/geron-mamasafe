"""
Daily Health Education Message Scheduler
Sends personalized daily messages to mothers based on their pregnancy stage or child's age
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
import pytz

from app.core.config import settings
from app.models.models import (
    Mother, Child, DailyMessageTemplate,
    PregnancyStage, ChildAgeGroup, Message
)
from app.services.twilio_service import TwilioMessageService

logger = logging.getLogger(__name__)


class DailyMessageScheduler:
    """Service for scheduling and sending daily health education messages"""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.twilio_service = TwilioMessageService()

    async def send_all_daily_messages(self) -> Dict:
        """
        Send daily messages to all active mothers
        This should be called by the scheduled task
        
        Returns:
            Summary of messages sent
        """
        results = {
            "total_mothers": 0,
            "messages_sent": 0,
            "messages_failed": 0,
            "errors": []
        }

        try:
            # Get all active mothers
            mothers_result = await self.db.execute(
                select(Mother).where(Mother.is_active == True)
            )
            mothers = mothers_result.scalars().all()
            
            results["total_mothers"] = len(mothers)
            
            for mother in mothers:
                try:
                    # Determine message based on mother's stage
                    message_content = await self._get_daily_message_for_mother(mother)
                    
                    if message_content:
                        # Determine channel (prefer WhatsApp, fallback to SMS)
                        channel = "whatsapp" if mother.whatsapp_number else "sms"
                        phone_number = mother.whatsapp_number or mother.phone_number
                        
                        # Send message
                        send_result = await self.twilio_service.send_daily_education_message(
                            phone_number,
                            message_content,
                            channel
                        )
                        
                        if send_result["success"]:
                            results["messages_sent"] += 1
                            
                            # Log message in database
                            await self._log_message(
                                mother_id=mother.id,
                                message_type="daily_education",
                                content=message_content,
                                direction="outbound",
                                channel=channel,
                                twilio_sid=send_result.get("message_sid")
                            )
                            
                            # Update mother's last message sent timestamp
                            mother.last_message_sent = datetime.utcnow()
                        else:
                            results["messages_failed"] += 1
                            results["errors"].append({
                                "mother_id": mother.id,
                                "error": send_result.get("error")
                            })
                    
                    # If mother has children, send child-specific messages too
                    if mother.children:
                        for child in mother.children:
                            if child.is_active:
                                child_message = await self._get_daily_message_for_child(child)
                                if child_message:
                                    channel = "whatsapp" if mother.whatsapp_number else "sms"
                                    phone_number = mother.whatsapp_number or mother.phone_number
                                    
                                    send_result = await self.twilio_service.send_message(
                                        phone_number,
                                        child_message,
                                        channel
                                    )
                                    
                                    if send_result["success"]:
                                        results["messages_sent"] += 1
                                    else:
                                        results["messages_failed"] += 1
                
                except Exception as e:
                    logger.error(f"Error sending message to mother {mother.id}: {str(e)}")
                    results["errors"].append({
                        "mother_id": mother.id,
                        "error": str(e)
                    })
            
            await self.db.commit()
            
            logger.info(f"Daily messages completed: {results}")
            return results
            
        except Exception as e:
            logger.error(f"Error in daily message scheduler: {str(e)}")
            await self.db.rollback()
            results["errors"].append({"general": str(e)})
            return results

    async def _get_daily_message_for_mother(self, mother: Mother) -> Optional[str]:
        """
        Get appropriate daily message for a mother based on her stage
        
        Args:
            mother: Mother object
            
        Returns:
            Message content string
        """
        # Determine stage
        if mother.pregnancy_stage == PregnancyStage.FIRST_TRIMESTER:
            stage = "first_trimester"
            category = "pregnancy"
        elif mother.pregnancy_stage == PregnancyStage.SECOND_TRIMESTER:
            stage = "second_trimester"
            category = "pregnancy"
        elif mother.pregnancy_stage == PregnancyStage.THIRD_TRIMESTER:
            stage = "third_trimester"
            category = "pregnancy"
        elif mother.pregnancy_stage == PregnancyStage.POSTPARTUM:
            stage = "postpartum"
            category = "postpartum"
        elif mother.pregnancy_stage == PregnancyStage.LABOR:
            stage = "labor"
            category = "pregnancy"
        else:
            # Default to pregnancy messages
            stage = "first_trimester"
            category = "pregnancy"

        # Get message template
        template = await self._get_message_template(category, stage)
        
        if template:
            return template.content
        
        # Fallback messages if no template found
        fallback_messages = {
            "first_trimester": "💚 First trimester tip: Take your folic acid daily and attend your antenatal appointments. Rest when you feel tired.",
            "second_trimester": "💚 Second trimester tip: Stay active with gentle exercises. Eat iron-rich foods and stay hydrated.",
            "third_trimester": "💚 Third trimester tip: Count your baby's movements daily. Pack your hospital bag and know the danger signs.",
            "postpartum": "💚 Postpartum tip: Rest when baby rests. Breastfeed frequently. Watch for signs of infection or heavy bleeding.",
            "labor": "💚 Labor tip: Stay calm and breathe. Have your hospital bag ready. Know when to go to the facility."
        }
        
        return fallback_messages.get(stage, "💚 Take care of yourself and attend your regular health check-ups!")

    async def _get_daily_message_for_child(self, child: Child) -> Optional[str]:
        """
        Get daily message for child care
        
        Args:
            child: Child object
            
        Returns:
            Message content string
        """
        # Determine age group
        if child.age_group == ChildAgeGroup.NEWBORN:
            stage = "newborn"
            category = "newborn_care"
        elif child.age_group == ChildAgeGroup.INFANT:
            stage = "infant"
            category = "child_care"
        elif child.age_group == ChildAgeGroup.TODDLER:
            stage = "toddler"
            category = "child_care"
        elif child.age_group == ChildAgeGroup.PRESCHOOL:
            stage = "preschool"
            category = "child_care"
        else:
            stage = "infant"
            category = "child_care"

        template = await self._get_message_template(category, stage)
        
        if template:
            return template.content
        
        # Fallback messages
        fallback_messages = {
            "newborn": "👶 Newborn care tip: Breastfeed exclusively for the first 6 months. Keep baby warm and practice skin-to-skin contact.",
            "infant": "👶 Infant care tip: Start introducing nutritious foods at 6 months while continuing breastfeeding.",
            "toddler": "👶 Toddler tip: Offer a variety of healthy foods. Ensure immunizations are up to date.",
            "preschool": "👶 Preschool tip: Encourage good hygiene habits. Monitor growth and development milestones."
        }
        
        return fallback_messages.get(stage, "👶 Keep your child healthy with good nutrition and regular health check-ups!")

    async def _get_message_template(self, category: str, stage: str) -> Optional[DailyMessageTemplate]:
        """
        Get a message template for category and stage
        
        Args:
            category: Message category
            stage: Pregnancy stage or child age group
            
        Returns:
            Message template or None
        """
        # Get today's day number (1-365)
        today = datetime.now()
        day_number = today.timetuple().tm_yday
        
        # Try to get template for this day
        result = await self.db.execute(
            select(DailyMessageTemplate).where(
                and_(
                    DailyMessageTemplate.category == category,
                    DailyMessageTemplate.stage == stage,
                    DailyMessageTemplate.is_active == True,
                    DailyMessageTemplate.language == "english"
                )
            ).order_by(DailyMessageTemplate.priority.desc())
        )
        
        templates = result.scalars().all()
        
        if templates:
            # Select template based on day number (cycle through available templates)
            index = (day_number - 1) % len(templates)
            return templates[index]
        
        return None

    async def _log_message(
        self,
        mother_id: int,
        message_type: str,
        content: str,
        direction: str,
        channel: str,
        twilio_sid: Optional[str] = None
    ):
        """Log a sent message in the database"""
        message = Message(
            mother_id=mother_id,
            message_type=message_type,
            content=content,
            direction=direction,
            channel=channel,
            status="sent",
            twilio_sid=twilio_sid,
            sent_at=datetime.utcnow()
        )
        self.db.add(message)


def create_scheduler(db_session: AsyncSession) -> DailyMessageScheduler:
    """Factory function to create scheduler instance"""
    return DailyMessageScheduler(db_session)
