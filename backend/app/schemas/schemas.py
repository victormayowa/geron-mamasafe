from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from app.models.models import (
    GenderEnum,
    RiskLevel,
    PregnancyStage,
    ChildAgeGroup,
    FacilityLevel,
    MessageStatus,
)


# ============ Health Center Schemas ============


class HealthCenterBase(BaseModel):
    name: str = Field(..., max_length=255)
    code: str = Field(..., max_length=50)
    facility_level: FacilityLevel
    district: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    address: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None


class HealthCenterCreate(HealthCenterBase):
    pass


class HealthCenter(HealthCenterBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


# ============ Mother Schemas ============


class MotherBase(BaseModel):
    phone_number: str = Field(..., max_length=20)
    whatsapp_number: Optional[str] = Field(None, max_length=20)
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    age: Optional[int] = None
    district: str = Field(..., max_length=100)
    address: Optional[str] = None
    emergency_contact: Optional[str] = Field(None, max_length=20)
    emergency_contact_name: Optional[str] = Field(None, max_length=200)

    pregnancy_stage: Optional[PregnancyStage] = None
    expected_due_date: Optional[datetime] = None

    risk_level: Optional[RiskLevel] = RiskLevel.LOW
    risk_factors: Optional[str] = None

    gravida: Optional[int] = None
    parity: Optional[int] = None
    previous_complications: Optional[str] = None
    blood_group: Optional[str] = Field(None, max_length=5)
    chronic_conditions: Optional[str] = None

    preferred_language: Optional[str] = Field("english", max_length=50)
    message_frequency: Optional[str] = Field("daily", max_length=20)
    preferred_message_time: Optional[str] = Field(None, max_length=5)


class MotherCreate(MotherBase):
    health_center_id: int
    consent_given: bool = True


class MotherUpdate(BaseModel):
    phone_number: Optional[str] = None
    whatsapp_number: Optional[str] = None
    pregnancy_stage: Optional[PregnancyStage] = None
    expected_due_date: Optional[datetime] = None
    risk_level: Optional[RiskLevel] = None
    risk_factors: Optional[str] = None
    is_high_risk: Optional[bool] = None
    last_interaction: Optional[datetime] = None


class Mother(MotherBase):
    id: int
    is_active: bool
    is_registered: bool
    is_high_risk: bool
    health_center_id: int
    registered_by_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_message_sent: Optional[datetime] = None
    last_interaction: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============ Child Schemas ============


class ChildBase(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    date_of_birth: datetime
    gender: GenderEnum
    age_group: Optional[ChildAgeGroup] = None

    birth_weight: Optional[float] = None
    birth_length: Optional[float] = None
    gestational_age: Optional[int] = None
    birth_type: Optional[str] = Field(None, max_length=50)
    complications_at_birth: Optional[str] = None
    apgar_score: Optional[int] = None

    risk_level: Optional[RiskLevel] = RiskLevel.LOW
    risk_factors: Optional[str] = None
    current_weight: Optional[float] = None
    current_height: Optional[float] = None
    immunization_status: Optional[str] = None

    feeding_method: Optional[str] = Field(None, max_length=50)
    feeding_notes: Optional[str] = None


class ChildCreate(ChildBase):
    mother_id: int


class Child(ChildBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============ Health Provider Schemas ============


class HealthProviderBase(BaseModel):
    employee_id: str = Field(..., max_length=50)
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    email: EmailStr
    phone: str = Field(..., max_length=20)
    role: str = Field(..., max_length=50)
    specialization: Optional[str] = Field(None, max_length=100)
    license_number: Optional[str] = Field(None, max_length=100)


class HealthProviderCreate(HealthProviderBase):
    password: str = Field(..., min_length=8)
    health_center_id: int


class HealthProviderLogin(BaseModel):
    email: EmailStr
    password: str


class HealthProvider(HealthProviderBase):
    id: int
    is_active: bool
    health_center_id: int
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class HealthProviderLogin(BaseModel):
    """Health provider login schema"""

    email: EmailStr
    password: str


# ============ Message Schemas ============


class MessageBase(BaseModel):
    message_type: str = Field(..., max_length=50)
    content: str = Field(..., max_length=5000)
    direction: str = Field(..., max_length=10)
    channel: str = Field(..., max_length=20)


class MessageCreate(MessageBase):
    mother_id: int


class Message(MessageBase):
    id: int
    status: MessageStatus
    twilio_sid: Optional[str] = None
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Consultation Schemas ============


class ConsultationQuery(BaseModel):
    """Incoming consultation query"""

    query: str = Field(..., min_length=1, max_length=2000)
    phone_number: str = Field(..., max_length=20)


class ConsultationBase(BaseModel):
    query: str = Field(..., max_length=2000)
    response: str = Field(..., max_length=5000)
    category: Optional[str] = Field(None, max_length=50)
    urgency_level: Optional[RiskLevel] = None
    ai_confidence: Optional[float] = Field(None, ge=0, le=1)
    requires_follow_up: Optional[bool] = False
    escalated: Optional[bool] = False


class Consultation(ConsultationBase):
    id: int
    mother_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Alert Schemas ============


class AlertBase(BaseModel):
    alert_type: str = Field(..., max_length=50)
    title: str = Field(..., max_length=255)
    description: str = Field(..., max_length=5000)
    severity: RiskLevel
    is_resolved: Optional[bool] = False


class AlertCreate(AlertBase):
    mother_id: Optional[int] = None
    child_id: Optional[int] = None


class Alert(AlertBase):
    id: int
    is_resolved: bool
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    notification_sent: bool
    notification_sent_at: Optional[datetime] = None
    created_at: datetime
    mother_id: Optional[int] = None
    child_id: Optional[int] = None

    class Config:
        from_attributes = True


# ============ Daily Message Template Schemas ============


class DailyMessageTemplateBase(BaseModel):
    title: str = Field(..., max_length=255)
    category: str = Field(..., max_length=50)
    stage: str = Field(..., max_length=50)
    content: str = Field(..., max_length=2000)
    day_number: Optional[int] = None
    priority: Optional[int] = 0
    language: Optional[str] = Field("english", max_length=50)


class DailyMessageTemplateCreate(DailyMessageTemplateBase):
    pass


class DailyMessageTemplate(DailyMessageTemplateBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============ Danger Sign Schemas ============


class DangerSignBase(BaseModel):
    category: str = Field(..., max_length=50)
    stage: str = Field(..., max_length=50)
    sign_name: str = Field(..., max_length=255)
    description: str = Field(..., max_length=2000)
    symptoms: Optional[str] = None
    severity: RiskLevel
    recommended_action: str = Field(..., max_length=2000)
    facility_level: FacilityLevel
    urgency: Optional[str] = Field(None, max_length=50)
    home_care_instructions: Optional[str] = None
    additional_notes: Optional[str] = None


class DangerSignCreate(DangerSignBase):
    pass


class DangerSign(DangerSignBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============ WhatsApp/SMS Webhook Schemas ============


class WhatsAppMessage(BaseModel):
    """Incoming WhatsApp message structure"""

    From: str
    To: str
    Body: str
    MessageSid: str
    AccountSid: str
    ProfileName: Optional[str] = None


class SMSMessage(BaseModel):
    """Incoming SMS message structure"""

    From: str
    To: str
    Body: str
    MessageSid: str
    AccountSid: str


# ============ Response Schemas ============


class APIResponse(BaseModel):
    """Generic API response"""

    success: bool
    message: str
    data: Optional[dict] = None


class PaginationResponse(BaseModel):
    """Pagination response"""

    total: int
    page: int
    size: int
    pages: int


class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""

    success: bool
    data: list
    pagination: PaginationResponse
