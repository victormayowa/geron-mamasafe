from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    Enum,
    Float,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class PatientType(str, enum.Enum):
    """Patient type categorization"""

    MOTHER = "mother"
    NEONATE = "neonate"
    INFANT = "infant"
    CHILD = "child"
    ADOLESCENT = "adolescent"


class TriageSeverity(str, enum.Enum):
    """Traffic light triage severity (IMCI standard)"""

    GREEN = "green"  # Home care
    YELLOW = "yellow"  # Visit PHC soon
    RED = "red"  # Emergency - go to hospital immediately


class GenderEnum(str, enum.Enum):
    """Gender enumeration"""

    MALE = "male"
    FEMALE = "female"


class RiskLevel(str, enum.Enum):
    """Risk level enumeration"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PregnancyStage(str, enum.Enum):
    """Pregnancy stage enumeration"""

    FIRST_TRIMESTER = "first_trimester"  # Weeks 1-12
    SECOND_TRIMESTER = "second_trimester"  # Weeks 13-26
    THIRD_TRIMESTER = "third_trimester"  # Weeks 27-40
    POSTPARTUM = "postpartum"  # After birth
    LABOR = "labor"  # In labor


class ChildAgeGroup(str, enum.Enum):
    """Child age group enumeration"""

    NEWBORN = "newborn"  # 0-28 days
    INFANT = "infant"  # 1-12 months
    TODDLER = "toddler"  # 1-3 years
    PRESCHOOL = "preschool"  # 3-5 years


class FacilityLevel(str, enum.Enum):
    """Healthcare facility level"""

    PRIMARY = "primary"  # Primary healthcare center
    SECONDARY = "secondary"  # General hospital
    TERTIARY = "tertiary"  # Specialist/teaching hospital


class MessageStatus(str, enum.Enum):
    """Message delivery status"""

    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    READ = "read"


class HealthCenter(Base):
    """Health center model"""

    __tablename__ = "health_centers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    facility_level = Column(Enum(FacilityLevel), nullable=False)
    district = Column(String(100), nullable=False, index=True)
    state = Column(String(100), nullable=False)
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    mothers = relationship("Mother", back_populates="health_center")
    health_providers = relationship("HealthProvider", back_populates="health_center")

    def __repr__(self):
        return f"<HealthCenter {self.name}>"


class Mother(Base):
    """Mother/Patient model"""

    __tablename__ = "mothers"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, nullable=False, index=True)
    whatsapp_number = Column(String(20), index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(DateTime)
    age = Column(Integer)
    district = Column(String(100), nullable=False, index=True)
    address = Column(Text)
    emergency_contact = Column(String(20))
    emergency_contact_name = Column(String(200))

    # Pregnancy information
    pregnancy_stage = Column(Enum(PregnancyStage))
    expected_due_date = Column(DateTime)
    registration_date = Column(DateTime(timezone=True), server_default=func.now())

    # Risk assessment
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.LOW)
    is_high_risk = Column(Boolean, default=False)
    risk_factors = Column(Text)  # JSON string of risk factors

    # Medical history
    gravida = Column(Integer)  # Number of pregnancies
    parity = Column(Integer)  # Number of births
    previous_complications = Column(Text)
    blood_group = Column(String(5))
    chronic_conditions = Column(Text)  # JSON string of conditions

    # Preferences
    preferred_language = Column(String(50), default="english")
    message_frequency = Column(String(20), default="daily")  # daily, twice_daily
    preferred_message_time = Column(String(5))  # HH:MM format

    # Status
    is_active = Column(Boolean, default=True)
    is_registered = Column(Boolean, default=False)
    consent_given = Column(Boolean, default=False)
    consent_date = Column(DateTime(timezone=True))

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_message_sent = Column(DateTime(timezone=True))
    last_interaction = Column(DateTime(timezone=True))

    # Foreign keys
    health_center_id = Column(
        Integer, ForeignKey("health_centers.id"), nullable=False, index=True
    )
    registered_by_id = Column(Integer, ForeignKey("health_providers.id"))

    # Relationships
    health_center = relationship("HealthCenter", back_populates="mothers")
    registered_by = relationship("HealthProvider", back_populates="registered_mothers")
    children = relationship("Child", back_populates="mother")
    messages = relationship("Message", back_populates="mother")
    consultations = relationship("Consultation", back_populates="mother")
    alerts = relationship("Alert", back_populates="mother")

    def __repr__(self):
        return f"<Mother {self.first_name} {self.last_name}>"


class Child(Base):
    """Child model"""

    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    age_group = Column(Enum(ChildAgeGroup))

    # Birth information
    birth_weight = Column(Float)  # in kg
    birth_length = Column(Float)  # in cm
    gestational_age = Column(Integer)  # in weeks
    birth_type = Column(String(50))  # vaginal, c-section
    complications_at_birth = Column(Text)
    apgar_score = Column(Integer)

    # Health status
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.LOW)
    is_high_risk = Column(Boolean, default=False)
    risk_factors = Column(Text)
    current_weight = Column(Float)
    current_height = Column(Float)
    immunization_status = Column(Text)  # JSON string

    # Feeding
    feeding_method = Column(String(50))  # breastfeeding, formula, mixed
    feeding_notes = Column(Text)

    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign keys
    mother_id = Column(Integer, ForeignKey("mothers.id"), nullable=False, index=True)

    # Relationships
    mother = relationship("Mother", back_populates="children")
    messages = relationship("ChildMessage", back_populates="child")
    alerts = relationship("Alert", back_populates="child")

    def __repr__(self):
        return f"<Child {self.first_name} {self.last_name}>"


class HealthProvider(Base):
    """Health provider/staff model"""

    __tablename__ = "health_providers"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(50), unique=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(
        String(50), nullable=False
    )  # nurse, doctor, midwife, community_health_worker
    specialization = Column(String(100))
    license_number = Column(String(100))

    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))

    # Foreign keys
    health_center_id = Column(
        Integer, ForeignKey("health_centers.id"), nullable=False, index=True
    )

    # Relationships
    health_center = relationship("HealthCenter", back_populates="health_providers")
    registered_mothers = relationship("Mother", back_populates="registered_by")

    def __repr__(self):
        return f"<HealthProvider {self.first_name} {self.last_name}>"


class Message(Base):
    """Message model for tracking sent messages"""

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    message_type = Column(
        String(50), nullable=False, index=True
    )  # daily_education, alert, response, reminder
    content = Column(Text, nullable=False)
    direction = Column(String(10), nullable=False)  # inbound, outbound
    channel = Column(String(20), nullable=False)  # whatsapp, sms
    status = Column(Enum(MessageStatus), default=MessageStatus.PENDING)
    twilio_sid = Column(String(100), index=True)
    error_message = Column(Text)
    sent_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))
    read_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Foreign keys
    mother_id = Column(Integer, ForeignKey("mothers.id"), nullable=False, index=True)

    # Relationships
    mother = relationship("Mother", back_populates="messages")

    def __repr__(self):
        return f"<Message {self.id} - {self.message_type}>"


class ChildMessage(Base):
    """Message model for child-specific messages"""

    __tablename__ = "child_messages"

    id = Column(Integer, primary_key=True, index=True)
    message_type = Column(String(50), nullable=False, index=True)
    content = Column(Text, nullable=False)
    direction = Column(String(10), nullable=False)
    channel = Column(String(20), nullable=False)
    status = Column(Enum(MessageStatus), default=MessageStatus.PENDING)
    twilio_sid = Column(String(100), index=True)
    sent_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Foreign keys
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False, index=True)
    mother_id = Column(Integer, ForeignKey("mothers.id"), nullable=False, index=True)

    # Relationships
    child = relationship("Child", back_populates="child_messages")
    mother = relationship("Mother")

    def __repr__(self):
        return f"<ChildMessage {self.id}>"


class Consultation(Base):
    """AI consultation/conversation model"""

    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    category = Column(
        String(50), index=True
    )  # danger_signs, general_inquiry, symptoms, advice
    urgency_level = Column(Enum(RiskLevel))
    ai_confidence = Column(Float)  # 0-1 confidence score
    requires_follow_up = Column(Boolean, default=False)
    escalated = Column(Boolean, default=False)
    escalated_to = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Foreign keys
    mother_id = Column(Integer, ForeignKey("mothers.id"), nullable=False, index=True)

    # Relationships
    mother = relationship("Mother", back_populates="consultations")

    def __repr__(self):
        return f"<Consultation {self.id}>"


class Alert(Base):
    """Alert model for danger signs and critical notifications"""

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(
        String(50), nullable=False, index=True
    )  # danger_sign, high_risk, appointment, immunization
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(Enum(RiskLevel), nullable=False)
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime(timezone=True))
    resolved_by = Column(String(200))
    notification_sent = Column(Boolean, default=False)
    notification_sent_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Foreign keys
    mother_id = Column(Integer, ForeignKey("mothers.id"), index=True)
    child_id = Column(Integer, ForeignKey("children.id"), index=True)
    adolescent_id = Column(Integer, ForeignKey("adolescents.id"), index=True)

    # Relationships
    mother = relationship("Mother", back_populates="alerts")
    child = relationship("Child", back_populates="alerts")
    adolescent = relationship("Adolescent", back_populates="alerts")

    def __repr__(self):
        return f"<Alert {self.id} - {self.alert_type}>"


class DailyMessageTemplate(Base):
    """Daily health education message templates"""

    __tablename__ = "daily_message_templates"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(
        String(50), nullable=False, index=True
    )  # pregnancy, postpartum, newborn, child_care
    stage = Column(
        String(50), nullable=False, index=True
    )  # matches pregnancy_stage or child_age_group
    content = Column(Text, nullable=False)
    day_number = Column(Integer)  # Day in sequence (e.g., day 1 of pregnancy week 1)
    priority = Column(Integer, default=0)  # Higher priority messages sent first
    is_active = Column(Boolean, default=True)
    language = Column(String(50), default="english")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<DailyMessageTemplate {self.title}>"


class DangerSign(Base):
    """Danger signs knowledge base"""

    __tablename__ = "danger_signs"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(
        String(50), nullable=False, index=True
    )  # maternal, neonatal, infant, child, adolescent
    stage = Column(
        String(50), nullable=False, index=True
    )  # pregnancy trimester, postpartum, age group
    sign_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    symptoms = Column(Text)  # JSON array of symptoms
    severity = Column(Enum(RiskLevel), nullable=False)
    triage_color = Column(Enum(TriageSeverity), nullable=False)  # IMCI traffic light
    recommended_action = Column(Text, nullable=False)
    facility_level = Column(Enum(FacilityLevel), nullable=False)  # where to go
    urgency = Column(String(50))  # immediate, same_day, within_24h, monitor
    home_care_instructions = Column(Text)  # What to do at home if applicable
    additional_notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<DangerSign {self.sign_name}>"


class Adolescent(Base):
    """Adolescent health tracking (10-19 years)"""

    __tablename__ = "adolescents"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    district = Column(String(100), nullable=False, index=True)

    # Health status
    is_pregnant = Column(Boolean, default=False)
    pregnancy_stage = Column(Enum(PregnancyStage), nullable=True)
    sexual_active = Column(Boolean, default=False)
    contraceptive_use = Column(String(100))
    mental_health_risk = Column(Boolean, default=False)
    substance_use = Column(Boolean, default=False)

    # Risk assessment
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.LOW)
    is_high_risk = Column(Boolean, default=False)
    risk_factors = Column(Text)

    # Status
    is_active = Column(Boolean, default=True)
    consent_given = Column(Boolean, default=False)
    parent_consent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_interaction = Column(DateTime(timezone=True))

    # Foreign keys
    health_center_id = Column(
        Integer, ForeignKey("health_centers.id"), nullable=False, index=True
    )

    # Relationships
    health_center = relationship("HealthCenter")
    messages = relationship("AdolescentMessage", back_populates="adolescent")
    alerts = relationship("Alert", back_populates="adolescent")

    def __repr__(self):
        return f"<Adolescent {self.first_name} {self.last_name}>"


class AdolescentMessage(Base):
    """Messages for adolescent health education"""

    __tablename__ = "adolescent_messages"

    id = Column(Integer, primary_key=True, index=True)
    message_type = Column(String(50), nullable=False, index=True)
    content = Column(Text, nullable=False)
    direction = Column(String(10), nullable=False)
    channel = Column(String(20), nullable=False)
    status = Column(Enum(MessageStatus), default=MessageStatus.PENDING)
    twilio_sid = Column(String(100), index=True)
    sent_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Foreign keys
    adolescent_id = Column(
        Integer, ForeignKey("adolescents.id"), nullable=False, index=True
    )

    # Relationships
    adolescent = relationship("Adolescent", back_populates="messages")

    def __repr__(self):
        return f"<AdolescentMessage {self.id}>"


class EMRIntegration(Base):
    """EMR integration tracking"""

    __tablename__ = "emr_integrations"

    id = Column(Integer, primary_key=True, index=True)
    emr_system = Column(String(100), nullable=False)  # DHIS2, OpenMRS, etc.
    patient_emr_id = Column(String(100), index=True)
    sync_type = Column(String(50), nullable=False)  # push, pull
    last_sync = Column(DateTime(timezone=True))
    sync_status = Column(String(50), default="pending")
    error_message = Column(Text)
    data_payload = Column(Text)  # JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<EMRIntegration {self.emr_system}>"
