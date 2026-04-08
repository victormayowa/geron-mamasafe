"""
Scheduled tasks runner
Runs daily message scheduling and other periodic tasks
"""

import asyncio
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session
from app.services.message_scheduler import DailyMessageScheduler
from app.core.config import settings

logger = logging.getLogger(__name__)


async def send_daily_messages():
    """Send daily messages to all mothers"""
    logger.info("Starting daily message dispatch...")
    
    async with async_session() as db:
        scheduler = DailyMessageScheduler(db)
        results = await scheduler.send_all_daily_messages()
        
        logger.info(f"Daily messages completed: {results}")


def start_scheduler():
    """Start the APScheduler for periodic tasks"""
    scheduler = AsyncIOScheduler()
    
    # Schedule daily messages
    scheduler.add_job(
        send_daily_messages,
        CronTrigger(hour=settings.DAILY_MESSAGE_HOUR, timezone=settings.DAILY_MESSAGE_TIMEZONE),
        id='daily_messages',
        name='Send daily health education messages',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info(f"Scheduler started. Daily messages scheduled for {settings.DAILY_MESSAGE_HOUR}:00 {settings.DAILY_MESSAGE_TIMEZONE}")
    
    return scheduler
