"""
Database seed script
Populates the database with initial danger signs and message templates
"""

import asyncio
import sys
from datetime import datetime

# Add backend to path
sys.path.insert(0, '/home/victormayowa/geron-mamasafe/backend')

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.core.database import Base
from app.models.models import (
    DangerSign, DailyMessageTemplate, HealthCenter,
    PregnancyStage, ChildAgeGroup, RiskLevel, FacilityLevel
)
from app.core.config import settings


async def seed_database():
    """Seed the database with initial data"""
    
    # Create engine
    engine = create_async_engine(settings.DATABASE_URL_SYNC.replace('postgresql://', 'postgresql+asyncpg://'))
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSession(engine) as session:
        print("🌱 Seeding database...")
        
        # ============ SEED DANGER SIGNS ============
        print("📋 Adding danger signs...")
        
        # Maternal danger signs - First Trimester
        first_trimester_signs = [
            DangerSign(
                category="maternal",
                stage="first_trimester",
                sign_name="Severe vaginal bleeding",
                description="Heavy bleeding that soaks more than one pad per hour",
                symptoms='["Heavy bleeding", "Passing large clots", "Dizziness", "Weakness"]',
                severity=RiskLevel.CRITICAL,
                recommended_action="Go immediately to secondary/tertiary facility. This could indicate miscarriage or ectopic pregnancy.",
                facility_level=FacilityLevel.SECONDARY,
                urgency="immediate",
                home_care_instructions="Lie down, keep calm, have someone stay with you. Do not delay seeking medical care."
            ),
            DangerSign(
                category="maternal",
                stage="first_trimester",
                sign_name="Severe abdominal pain",
                description="Persistent, severe pain in the lower abdomen",
                symptoms='["Sharp pain", "Cramping", "Pain on one side", "Persistent pain"]',
                severity=RiskLevel.HIGH,
                recommended_action="Seek immediate medical attention. Could indicate ectopic pregnancy or miscarriage.",
                facility_level=FacilityLevel.SECONDARY,
                urgency="immediate",
                home_care_instructions="Rest in comfortable position. Do not take pain medication before seeing a doctor."
            ),
            DangerSign(
                category="maternal",
                stage="first_trimester",
                sign_name="Severe nausea and vomiting",
                description="Inability to keep down food or fluids (Hyperemesis gravidarum)",
                symptoms='["Vomiting multiple times daily", "Unable to eat", "Weight loss", "Dehydration"]',
                severity=RiskLevel.HIGH,
                recommended_action="Visit primary healthcare center. May need IV fluids and anti-nausea medication.",
                facility_level=FacilityLevel.PRIMARY,
                urgency="same_day",
                home_care_instructions="Sip small amounts of clear fluids frequently. Eat bland foods. Rest."
            ),
        ]
        
        # Maternal danger signs - Second Trimester
        second_trimester_signs = [
            DangerSign(
                category="maternal",
                stage="second_trimester",
                sign_name="Vaginal bleeding",
                description="Any bleeding from the vagina",
                symptoms='["Light or heavy bleeding", "Spotting", "Brown or red discharge"]',
                severity=RiskLevel.HIGH,
                recommended_action="Go to secondary facility immediately. May indicate placenta problems.",
                facility_level=FacilityLevel.SECONDARY,
                urgency="immediate",
                home_care_instructions="Lie on your left side. Do not use tampons. Have someone accompany you."
            ),
            DangerSign(
                category="maternal",
                stage="second_trimester",
                sign_name="Severe headache",
                description="Persistent, severe headache that does not go away",
                symptoms='["Persistent headache", "Visual disturbances", "Blurred vision", "Seeing spots"]',
                severity=RiskLevel.HIGH,
                recommended_action="Visit primary healthcare immediately. Could be sign of preeclampsia.",
                facility_level=FacilityLevel.PRIMARY,
                urgency="same_day",
                home_care_instructions="Rest in dark, quiet room. Monitor for other symptoms."
            ),
            DangerSign(
                category="maternal",
                stage="second_trimester",
                sign_name="Decreased fetal movement",
                description="Noticeable reduction in baby's movements",
                symptoms='["Less kicking", "Less movement than usual", "No movement for several hours"]',
                severity=RiskLevel.HIGH,
                recommended_action="Go to secondary facility immediately for fetal monitoring.",
                facility_level=FacilityLevel.SECONDARY,
                urgency="immediate",
                home_care_instructions="Lie on left side and count movements. If less than 10 in 2 hours, go to hospital."
            ),
        ]
        
        # Maternal danger signs - Third Trimester
        third_trimester_signs = [
            DangerSign(
                category="maternal",
                stage="third_trimester",
                sign_name="Severe headache with visual changes",
                description="Severe headache accompanied by vision problems - sign of preeclampsia",
                symptoms='["Severe headache", "Blurred vision", "Seeing spots", "Light sensitivity"]',
                severity=RiskLevel.CRITICAL,
                recommended_action="Go to tertiary facility IMMEDIATELY. This is a medical emergency.",
                facility_level=FacilityLevel.TERTIARY,
                urgency="immediate",
                home_care_instructions="Have someone drive you. Do not drive yourself. Lie on left side during transport."
            ),
            DangerSign(
                category="maternal",
                stage="third_trimester",
                sign_name="Difficulty breathing",
                description="Shortness of breath or difficulty breathing",
                symptoms='["Shortness of breath", "Rapid breathing", "Chest pain", "Palpitations"]',
                severity=RiskLevel.CRITICAL,
                recommended_action="Go to secondary/tertiary facility immediately.",
                facility_level=FacilityLevel.SECONDARY,
                urgency="immediate",
                home_care_instructions="Sit upright. Stay calm. Have someone drive you to hospital."
            ),
            DangerSign(
                category="maternal",
                stage="third_trimester",
                sign_name="Reduced fetal movement",
                description="Significantly decreased or absent fetal movements",
                symptoms='["No movement for 12+ hours", "Significantly reduced movement"]',
                severity=RiskLevel.CRITICAL,
                recommended_action="Go to secondary facility IMMEDIATELY for fetal monitoring.",
                facility_level=FacilityLevel.SECONDARY,
                urgency="immediate",
                home_care_instructions="Drink cold water, lie on left side and count movements."
            ),
        ]
        
        # Postpartum danger signs
        postpartum_signs = [
            DangerSign(
                category="maternal",
                stage="postpartum",
                sign_name="Heavy bleeding after birth",
                description="Soaking more than one pad per hour after delivery",
                symptoms='["Heavy bleeding", "Large clots", "Foul-smelling discharge", "Dizziness"]',
                severity=RiskLevel.CRITICAL,
                recommended_action="Emergency! Go to secondary/tertiary facility immediately. Risk of postpartum hemorrhage.",
                facility_level=FacilityLevel.SECONDARY,
                urgency="immediate",
                home_care_instructions="Massage uterus. Breastfeed to help uterus contract. Go to hospital."
            ),
            DangerSign(
                category="maternal",
                stage="postpartum",
                sign_name="Thoughts of harming baby or self",
                description="Postpartum depression or psychosis symptoms",
                symptoms='["Sadness", "Hopelessness", "Thoughts of harm", "Anxiety"]',
                severity=RiskLevel.CRITICAL,
                recommended_action="Seek immediate help from primary healthcare provider or mental health professional.",
                facility_level=FacilityLevel.PRIMARY,
                urgency="immediate",
                home_care_instructions="Tell someone immediately. You are not alone. Help is available."
            ),
        ]
        
        # Neonatal danger signs
        neonatal_signs = [
            DangerSign(
                category="neonatal",
                stage="newborn",
                sign_name="Not feeding well",
                description="Baby is unable to feed or feeding poorly",
                symptoms='["Not sucking", "Weak suck", "Refusing breast"]',
                severity=RiskLevel.HIGH,
                recommended_action="Go to primary healthcare center immediately. Newborn needs nutrition urgently.",
                facility_level=FacilityLevel.PRIMARY,
                urgency="immediate",
                home_care_instructions="Try feeding with cup and spoon if baby won't breastfeed. Keep baby warm."
            ),
            DangerSign(
                category="neonatal",
                stage="newborn",
                sign_name="Convulsions",
                description="Baby having seizures or fits",
                symptoms='["Jerking movements", "Stiffening", "Loss of consciousness"]',
                severity=RiskLevel.CRITICAL,
                recommended_action="EXTREME EMERGENCY! Go to tertiary facility immediately.",
                facility_level=FacilityLevel.TERTIARY,
                urgency="immediate",
                home_care_instructions="Place baby on side. Do not put anything in mouth. Go to hospital."
            ),
            DangerSign(
                category="neonatal",
                stage="newborn",
                sign_name="Fast breathing",
                description="Breathing rate more than 60 breaths per minute",
                symptoms='["Rapid breathing", "Grunting", "Nasal flaring", "Chest indrawing"]',
                severity=RiskLevel.HIGH,
                recommended_action="Go to secondary facility immediately. May indicate respiratory distress.",
                facility_level=FacilityLevel.SECONDARY,
                urgency="immediate",
                home_care_instructions="Keep baby in comfortable position. Keep warm. Go to hospital."
            ),
            DangerSign(
                category="neonatal",
                stage="newborn",
                sign_name="Fever (37.5°C or higher)",
                description="Elevated temperature in newborn",
                symptoms='["Hot body", "Warm to touch", "Flushed", "Sweating"]',
                severity=RiskLevel.HIGH,
                recommended_action="Go to primary healthcare center immediately. Fever in newborn is serious.",
                facility_level=FacilityLevel.PRIMARY,
                urgency="immediate",
                home_care_instructions="Undress baby lightly. Keep room warm but not hot. Go to hospital."
            ),
        ]
        
        all_danger_signs = (
            first_trimester_signs + 
            second_trimester_signs + 
            third_trimester_signs + 
            postpartum_signs + 
            neonatal_signs
        )
        
        for sign in all_danger_signs:
            session.add(sign)
        
        print(f"✅ Added {len(all_danger_signs)} danger signs")
        
        # ============ SEED DAILY MESSAGE TEMPLATES ============
        print("📝 Adding daily message templates...")
        
        pregnancy_messages = [
            # First Trimester
            DailyMessageTemplate(
                title="Importance of Folic Acid",
                category="pregnancy",
                stage="first_trimester",
                content="💚 First trimester tip: Take your folic acid daily! It helps prevent birth defects. Eat leafy greens, beans, and citrus fruits. Attend your antenatal appointments regularly.",
                day_number=1,
                priority=10
            ),
            DailyMessageTemplate(
                title="Managing Morning Sickness",
                category="pregnancy",
                stage="first_trimester",
                content="💚 Morning sickness tip: Eat small frequent meals. Keep crackers by your bed. Ginger tea can help. If vomiting is severe, see your healthcare provider.",
                day_number=2,
                priority=9
            ),
            DailyMessageTemplate(
                title="Rest and Nutrition",
                category="pregnancy",
                stage="first_trimester",
                content="💚 Your body is working hard! Rest when tired. Eat iron-rich foods like spinach and beans. Drink plenty of water. Avoid alcohol and smoking.",
                day_number=3,
                priority=8
            ),
            
            # Second Trimester
            DailyMessageTemplate(
                title="Feeling Baby Move",
                category="pregnancy",
                stage="second_trimester",
                content="💚 You should feel baby moving now! Count movements daily. If movements decrease significantly, contact your healthcare provider immediately.",
                day_number=1,
                priority=10
            ),
            DailyMessageTemplate(
                title="Stay Active",
                category="pregnancy",
                stage="second_trimester",
                content="💚 Gentle exercise is good! Walk daily. Prenatal yoga helps. Avoid heavy lifting. Stay hydrated. Eat calcium-rich foods for baby's bones.",
                day_number=2,
                priority=8
            ),
            
            # Third Trimester
            DailyMessageTemplate(
                title="Know Danger Signs",
                category="pregnancy",
                stage="third_trimester",
                content="⚠️ Third trimester alert: Know danger signs - severe headache, blurred vision, heavy bleeding, reduced baby movements. Go to hospital immediately if you experience these.",
                day_number=1,
                priority=10
            ),
            DailyMessageTemplate(
                title="Prepare for Delivery",
                category="pregnancy",
                stage="third_trimester",
                content="💚 Pack your hospital bag now! Include: clothes for you and baby, towels, sanitary pads, and delivery plan. Know your route to the hospital.",
                day_number=2,
                priority=9
            ),
            
            # Postpartum
            DailyMessageTemplate(
                title="Breastfeeding Benefits",
                category="postpartum",
                stage="postpartum",
                content="💚 Breastfeed exclusively for 6 months! It gives baby perfect nutrition and protects from infections. Feed on demand, day and night.",
                day_number=1,
                priority=10
            ),
            DailyMessageTemplate(
                title="Postpartum Rest",
                category="postpartum",
                stage="postpartum",
                content="💚 Rest when baby rests! Accept help from family. Eat nutritious meals. Watch for heavy bleeding or fever - seek care if present.",
                day_number=2,
                priority=9
            ),
        ]
        
        child_care_messages = [
            # Newborn
            DailyMessageTemplate(
                title="Skin-to-Skin Contact",
                category="child_care",
                stage="newborn",
                content="👶 Newborn tip: Practice skin-to-skin contact! It keeps baby warm, promotes bonding, and helps with breastfeeding. Keep baby's head covered.",
                day_number=1,
                priority=10
            ),
            DailyMessageTemplate(
                title="Umbilical Cord Care",
                category="child_care",
                stage="newborn",
                content="👶 Cord care: Keep it clean and dry. Fold diaper below cord. Don't apply traditional substances. If red, swollen, or pus appears, see a doctor.",
                day_number=2,
                priority=9
            ),
            
            # Infant
            DailyMessageTemplate(
                title="Exclusive Breastfeeding",
                category="child_care",
                stage="infant",
                content="👶 For first 6 months: Only breast milk! No water, no other foods. Breast milk has everything baby needs and protects from diseases.",
                day_number=1,
                priority=10
            ),
            
            # Toddler
            DailyMessageTemplate(
                title="Introducing Foods",
                category="child_care",
                stage="toddler",
                content="👶 At 6 months: Start nutritious foods! Mashed beans, sweet potato, avocado. Continue breastfeeding. Introduce one food at a time.",
                day_number=1,
                priority=10
            ),
        ]
        
        all_templates = pregnancy_messages + child_care_messages
        
        for template in all_templates:
            session.add(template)
        
        print(f"✅ Added {len(all_templates)} message templates")
        
        # ============ SEED HEALTH CENTERS ============
        print("🏥 Adding sample health centers...")
        
        sample_centers = [
            HealthCenter(
                name="Primary Healthcare Center - Example",
                code="PHC001",
                facility_level=FacilityLevel.PRIMARY,
                district="Central District",
                state="Example State",
                address="123 Health Street",
                phone="+1234567890",
                is_active=True
            ),
            HealthCenter(
                name="General Hospital - Example",
                code="GH001",
                facility_level=FacilityLevel.SECONDARY,
                district="Central District",
                state="Example State",
                address="456 Hospital Avenue",
                phone="+1234567891",
                is_active=True
            ),
        ]
        
        for center in sample_centers:
            session.add(center)
        
        print(f"✅ Added {len(sample_centers)} health centers")
        
        # Commit all changes
        await session.commit()
        print("\n✅ Database seeding completed successfully!")


if __name__ == "__main__":
    asyncio.run(seed_database())
