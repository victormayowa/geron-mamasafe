"""
Messages API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.core.database import get_db
from app.models.models import Message, MessageStatus
from app.schemas.schemas import Message as MessageSchema

router = APIRouter()


@router.get("/mother/{mother_id}")
async def get_mother_messages(
    mother_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get all messages for a mother"""
    
    query = (
        select(Message)
        .where(Message.mother_id == mother_id)
        .order_by(Message.created_at.desc())
    )
    
    # Get total count
    count_result = await db.execute(
        select(Message).where(Message.mother_id == mother_id)
    )
    total = len(count_result.scalars().all())
    
    # Apply pagination
    offset = (page - 1) * size
    query = query.offset(offset).limit(size)
    
    result = await db.execute(query)
    messages = result.scalars().all()
    
    return {
        "success": True,
        "data": [MessageSchema.model_validate(m) for m in messages],
        "pagination": {
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size
        }
    }
