"""
Comprehensive danger signs knowledge base - IMCI/WHO Standard
Maternal, Neonatal, Infant, Child Under-5, and Adolescent
Uses TRAFFIC LIGHT TRIAGE: RED (Emergency), YELLOW (Urgent), GREEN (Home)
"""

from typing import Dict, List, Optional
from app.models.models import (
    RiskLevel,
    FacilityLevel,
    PregnancyStage,
    ChildAgeGroup,
    TriageSeverity,
)


class DangerSignsDatabase:
    """Static database of all danger signs - IMCI/WHO based"""

    # ============ MATERNAL DANGER SIGNS ============

    MATERNAL_DANGER_SIGNS = {
        PregnancyStage.FIRST_TRIMESTER: [
            {
                "sign_name": "Severe vaginal bleeding",
                "description": "Heavy bleeding that soaks more than one pad per hour",
                "symptoms": [
                    "Heavy bleeding",
                    "Passing large clots",
                    "Dizziness",
                    "Weakness",
                ],
                "severity": RiskLevel.CRITICAL,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital IMMEDIATELY. This could indicate miscarriage or ectopic pregnancy.",
                "facility_level": FacilityLevel.SECONDARY,
                "urgency": "immediate",
                "home_care_instructions": "Lie down, keep calm, have someone stay with you. Do not delay seeking medical care.",
            },
            {
                "sign_name": "Severe abdominal pain",
                "description": "Persistent, severe pain in the lower abdomen",
                "symptoms": [
                    "Sharp pain",
                    "Cramping",
                    "Pain on one side",
                    "Persistent pain",
                ],
                "severity": RiskLevel.HIGH,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital immediately. Could indicate ectopic pregnancy.",
                "facility_level": FacilityLevel.SECONDARY,
                "urgency": "immediate",
                "home_care_instructions": "Rest in comfortable position. Do not take pain medication before seeing a doctor.",
            },
            {
                "sign_name": "Severe nausea and vomiting",
                "description": "Inability to keep down food or fluids (Hyperemesis gravidarum)",
                "symptoms": [
                    "Vomiting multiple times daily",
                    "Unable to eat",
                    "Weight loss",
                    "Dehydration",
                    "Dark urine",
                ],
                "severity": RiskLevel.HIGH,
                "triage_color": TriageSeverity.YELLOW,
                "recommended_action": "🟡 Visit health center TODAY. May need IV fluids and medication.",
                "facility_level": FacilityLevel.PRIMARY,
                "urgency": "same_day",
                "home_care_instructions": "Sip small amounts of clear fluids frequently. Eat bland foods like crackers. Rest and avoid triggers.",
            },
            {
                "sign_name": "Fever above 38°C",
                "description": "Elevated body temperature that may indicate infection",
                "symptoms": ["High temperature", "Chills", "Sweating", "Body aches"],
                "severity": RiskLevel.MEDIUM,
                "triage_color": TriageSeverity.YELLOW,
                "recommended_action": "🟡 Visit health center TODAY. Fever in pregnancy needs evaluation.",
                "facility_level": FacilityLevel.PRIMARY,
                "urgency": "within_24h",
                "home_care_instructions": "Take paracetamol (acetaminophen). Drink plenty of fluids. Rest. Monitor temperature.",
            },
            {
                "sign_name": "Painful urination",
                "description": "Burning or pain during urination, may indicate urinary tract infection",
                "symptoms": [
                    "Burning sensation",
                    "Frequent urination",
                    "Cloudy urine",
                    "Lower abdominal pain",
                ],
                "severity": RiskLevel.MEDIUM,
                "triage_color": TriageSeverity.YELLOW,
                "recommended_action": "🟡 Visit health center for urine test and possible antibiotics.",
                "facility_level": FacilityLevel.PRIMARY,
                "urgency": "within_24h",
                "home_care_instructions": "Drink plenty of water. Avoid caffeine. Urinate frequently.",
            },
            {
                "sign_name": "Mild headache",
                "description": "Common in first trimester due to hormonal changes",
                "symptoms": ["Mild headache", "Fatigue", "Dizziness"],
                "severity": RiskLevel.LOW,
                "triage_color": TriageSeverity.GREEN,
                "recommended_action": "🟢 HOME CARE is safe. Rest and stay hydrated.",
                "facility_level": FacilityLevel.PRIMARY,
                "urgency": "monitor",
                "home_care_instructions": "Rest in dark, quiet room. Drink water. Eat small frequent meals. Take paracetamol if needed.",
            },
        ],
        PregnancyStage.SECOND_TRIMESTER: [
            {
                "sign_name": "Vaginal bleeding",
                "description": "Any bleeding from the vagina",
                "symptoms": [
                    "Light or heavy bleeding",
                    "Spotting",
                    "Brown or red discharge",
                ],
                "severity": RiskLevel.HIGH,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital immediately. May indicate placenta problems.",
                "facility_level": FacilityLevel.SECONDARY,
                "urgency": "immediate",
                "home_care_instructions": "Lie on your left side. Do not use tampons. Have someone accompany you.",
            },
            {
                "sign_name": "Severe headache with vision changes",
                "description": "Persistent, severe headache with blurred vision - sign of preeclampsia",
                "symptoms": [
                    "Persistent headache",
                    "Blurred vision",
                    "Seeing spots",
                    "Light sensitivity",
                ],
                "severity": RiskLevel.HIGH,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital immediately. Could be preeclampsia.",
                "facility_level": FacilityLevel.SECONDARY,
                "urgency": "immediate",
                "home_care_instructions": "Rest on left side. Do not drive yourself. Have someone take you to hospital.",
            },
            {
                "sign_name": "Sudden swelling of face/hands",
                "description": "Sudden swelling may indicate preeclampsia",
                "symptoms": ["Facial swelling", "Hand swelling", "Rapid weight gain"],
                "severity": RiskLevel.HIGH,
                "triage_color": TriageSeverity.YELLOW,
                "recommended_action": "🟡 Visit health center TODAY. Check blood pressure for preeclampsia.",
                "facility_level": FacilityLevel.PRIMARY,
                "urgency": "same_day",
                "home_care_instructions": "Rest on left side. Elevate feet. Monitor blood pressure if available.",
            },
            {
                "sign_name": "Decreased fetal movement",
                "description": "Noticeable reduction in baby's movements",
                "symptoms": [
                    "Less kicking",
                    "Less movement than usual",
                    "No movement for several hours",
                ],
                "severity": RiskLevel.HIGH,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital immediately for fetal monitoring.",
                "facility_level": FacilityLevel.SECONDARY,
                "urgency": "immediate",
                "home_care_instructions": "Lie on left side. Drink cold water. Count movements. If less than 10 in 2 hours, go to hospital.",
            },
            {
                "sign_name": "Fluid leaking from vagina",
                "description": "Leaking of amniotic fluid (water breaking)",
                "symptoms": ["Continuous leaking", "Clear fluid", "Gush of fluid"],
                "severity": RiskLevel.HIGH,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital immediately. Risk of infection.",
                "facility_level": FacilityLevel.SECONDARY,
                "urgency": "immediate",
                "home_care_instructions": "Do not insert anything into vagina. Note time fluid started. Go to hospital.",
            },
        ],
        PregnancyStage.THIRD_TRIMESTER: [
            {
                "sign_name": "Severe headache with blurred vision",
                "description": "Severe headache with vision problems - sign of severe preeclampsia",
                "symptoms": [
                    "Severe headache",
                    "Blurred vision",
                    "Seeing spots",
                    "Light sensitivity",
                ],
                "severity": RiskLevel.CRITICAL,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital IMMEDIATELY. This is life-threatening.",
                "facility_level": FacilityLevel.TERTIARY,
                "urgency": "immediate",
                "home_care_instructions": "Have someone drive you. Do not drive yourself. Lie on left side during transport.",
            },
            {
                "sign_name": "Severe upper abdominal pain",
                "description": "Severe pain in upper right abdomen - sign of HELLP syndrome",
                "symptoms": [
                    "Upper right pain",
                    "Nausea",
                    "Shoulder pain",
                    "Feeling very unwell",
                ],
                "severity": RiskLevel.CRITICAL,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital IMMEDIATELY. This is HELLP syndrome.",
                "facility_level": FacilityLevel.TERTIARY,
                "urgency": "immediate",
                "home_care_instructions": "Do not eat or drink in case emergency surgery is needed. Go to hospital now.",
            },
            {
                "sign_name": "Difficulty breathing",
                "description": "Shortness of breath or difficulty breathing",
                "symptoms": [
                    "Shortness of breath",
                    "Rapid breathing",
                    "Chest pain",
                    "Palpitations",
                ],
                "severity": RiskLevel.CRITICAL,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital IMMEDIATELY.",
                "facility_level": FacilityLevel.SECONDARY,
                "urgency": "immediate",
                "home_care_instructions": "Sit upright. Stay calm. Have someone drive you to hospital.",
            },
            {
                "sign_name": "Regular contractions before 37 weeks",
                "description": "Regular contractions indicating possible preterm labor",
                "symptoms": [
                    "Regular contractions",
                    "Lower back pain",
                    "Pelvic pressure",
                    "Menstrual-like cramps",
                ],
                "severity": RiskLevel.HIGH,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital immediately. Preterm labor needs intervention.",
                "facility_level": FacilityLevel.SECONDARY,
                "urgency": "immediate",
                "home_care_instructions": "Lie on left side. Drink water. Time contractions. Go to hospital.",
            },
            {
                "sign_name": "Reduced fetal movement",
                "description": "Significantly decreased or absent fetal movements",
                "symptoms": [
                    "No movement for 12+ hours",
                    "Significantly reduced movement",
                ],
                "severity": RiskLevel.CRITICAL,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital IMMEDIATELY for fetal monitoring.",
                "facility_level": FacilityLevel.SECONDARY,
                "urgency": "immediate",
                "home_care_instructions": "Drink cold water, lie on left side and count movements. If less than 10 in 2 hours, go now.",
            },
            {
                "sign_name": "Vaginal bleeding with pain",
                "description": "Bleeding with abdominal pain - possible placental abruption",
                "symptoms": [
                    "Bleeding",
                    "Abdominal pain",
                    "Back pain",
                    "Frequent contractions",
                ],
                "severity": RiskLevel.CRITICAL,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital IMMEDIATELY.",
                "facility_level": FacilityLevel.TERTIARY,
                "urgency": "immediate",
                "home_care_instructions": "Lie down. Have someone drive you. Do not eat or drink.",
            },
        ],
        PregnancyStage.LABOR: [
            {
                "sign_name": "Prolonged labor (>12 hours)",
                "description": "Labor lasting more than 12 hours without progress",
                "symptoms": [
                    "Contractions without progress",
                    "Exhaustion",
                    "Dehydration",
                ],
                "severity": RiskLevel.HIGH,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Medical intervention needed at hospital.",
                "facility_level": FacilityLevel.SECONDARY,
                "urgency": "immediate",
                "home_care_instructions": "If at home, go to hospital immediately.",
            },
            {
                "sign_name": "Heavy bleeding during labor",
                "description": "Heavy bleeding before or during labor",
                "symptoms": ["Heavy bleeding", "Large clots", "Dizziness"],
                "severity": RiskLevel.CRITICAL,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital IMMEDIATELY.",
                "facility_level": FacilityLevel.TERTIARY,
                "urgency": "immediate",
                "home_care_instructions": "Lie down. Have someone drive you to hospital.",
            },
            {
                "sign_name": "Cord prolapse",
                "description": "Umbilical cord comes out before the baby",
                "symptoms": ["Cord visible in vagina", "Sudden fetal distress"],
                "severity": RiskLevel.CRITICAL,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EXTREME EMERGENCY! Go to hospital IMMEDIATELY.",
                "facility_level": FacilityLevel.TERTIARY,
                "urgency": "immediate",
                "home_care_instructions": "Get on hands and knees with bottom in air. Call emergency services. Do not push cord back.",
            },
            {
                "sign_name": "Meconium-stained fluid",
                "description": "Green or brown amniotic fluid indicating baby passed stool",
                "symptoms": ["Green fluid", "Brown fluid", "Foul smell"],
                "severity": RiskLevel.HIGH,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital immediately. Baby may need special care.",
                "facility_level": FacilityLevel.SECONDARY,
                "urgency": "immediate",
                "home_care_instructions": "Go to hospital. Note time membranes ruptured.",
            },
        ],
        PregnancyStage.POSTPARTUM: [
            {
                "sign_name": "Heavy bleeding after birth",
                "description": "Soaking more than one pad per hour after delivery",
                "symptoms": ["Heavy bleeding", "Large clots", "Dizziness", "Weakness"],
                "severity": RiskLevel.CRITICAL,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital IMMEDIATELY. Risk of postpartum hemorrhage.",
                "facility_level": FacilityLevel.SECONDARY,
                "urgency": "immediate",
                "home_care_instructions": "Massage uterus (firm mass in lower abdomen). Breastfeed to help contract. Go to hospital.",
            },
            {
                "sign_name": "Fever after delivery (>38°C)",
                "description": "Temperature above 38°C after birth - sign of infection",
                "symptoms": [
                    "Fever",
                    "Chills",
                    "Abdominal pain",
                    "Foul-smelling discharge",
                ],
                "severity": RiskLevel.HIGH,
                "triage_color": TriageSeverity.YELLOW,
                "recommended_action": "🟡 Visit health center TODAY. May indicate infection needing antibiotics.",
                "facility_level": FacilityLevel.PRIMARY,
                "urgency": "same_day",
                "home_care_instructions": "Keep taking prescribed medications. Rest. Drink fluids.",
            },
            {
                "sign_name": "Severe abdominal pain after birth",
                "description": "Persistent severe pain after delivery",
                "symptoms": [
                    "Severe pain",
                    "Abdominal swelling",
                    "Tenderness",
                    "Fever",
                ],
                "severity": RiskLevel.HIGH,
                "triage_color": TriageSeverity.YELLOW,
                "recommended_action": "🟡 Visit health center TODAY. May indicate infection or retained placenta.",
                "facility_level": FacilityLevel.SECONDARY,
                "urgency": "same_day",
                "home_care_instructions": "Rest. Take prescribed pain medication. Monitor temperature.",
            },
            {
                "sign_name": "Thoughts of harming baby or self",
                "description": "Postpartum depression or psychosis symptoms",
                "symptoms": [
                    "Sadness",
                    "Hopelessness",
                    "Thoughts of harm",
                    "Anxiety",
                    "Unable to care for baby",
                ],
                "severity": RiskLevel.CRITICAL,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Seek immediate help from healthcare provider.",
                "facility_level": FacilityLevel.PRIMARY,
                "urgency": "immediate",
                "home_care_instructions": "Tell someone immediately. You are not alone. Help is available.",
            },
            {
                "sign_name": "Red, swollen, painful breast",
                "description": "Signs of mastitis or breast infection",
                "symptoms": ["Breast pain", "Redness", "Swelling", "Warmth", "Fever"],
                "severity": RiskLevel.MEDIUM,
                "triage_color": TriageSeverity.YELLOW,
                "recommended_action": "🟡 Visit health center. May need antibiotics.",
                "facility_level": FacilityLevel.PRIMARY,
                "urgency": "within_24h",
                "home_care_instructions": "Continue breastfeeding. Apply warm compress. Rest. Massage gently.",
            },
            {
                "sign_name": "Mild sadness (baby blues)",
                "description": "Common mood changes in first few days after birth",
                "symptoms": ["Mood swings", "Mild sadness", "Crying"],
                "severity": RiskLevel.LOW,
                "triage_color": TriageSeverity.GREEN,
                "recommended_action": "🟢 HOME CARE is safe. Normal in first 2 weeks. Seek help if persists.",
                "facility_level": FacilityLevel.PRIMARY,
                "urgency": "monitor",
                "home_care_instructions": "Rest when baby sleeps. Accept help from family. Talk to someone. If symptoms last >2 weeks, see doctor.",
            },
        ],
    }

    # ============ NEONATAL DANGER SIGNS (0-28 days) - IMCI ============

    NEONATAL_DANGER_SIGNS = [
        {
            "sign_name": "Not feeding well",
            "description": "Baby is unable to feed or feeding poorly",
            "symptoms": [
                "Not sucking",
                "Weak suck",
                "Refusing breast",
                "Feeding less than half normal",
            ],
            "severity": RiskLevel.HIGH,
            "triage_color": TriageSeverity.RED,
            "recommended_action": "🔴 EMERGENCY! Go to health center IMMEDIATELY. Newborn needs nutrition urgently.",
            "facility_level": FacilityLevel.PRIMARY,
            "urgency": "immediate",
            "home_care_instructions": "Try feeding with cup and spoon if baby won't breastfeed. Keep baby warm.",
        },
        {
            "sign_name": "Convulsions",
            "description": "Baby having seizures or fits",
            "symptoms": [
                "Jerking movements",
                "Stiffening",
                "Loss of consciousness",
                "Eye rolling",
            ],
            "severity": RiskLevel.CRITICAL,
            "triage_color": TriageSeverity.RED,
            "recommended_action": "🔴 EXTREME EMERGENCY! Go to hospital IMMEDIATELY.",
            "facility_level": FacilityLevel.TERTIARY,
            "urgency": "immediate",
            "home_care_instructions": "Place baby on side. Do not put anything in mouth. Clear area. Go to hospital.",
        },
        {
            "sign_name": "Fast breathing (>60/min)",
            "description": "Breathing rate more than 60 breaths per minute",
            "symptoms": [
                "Rapid breathing",
                "Grunting",
                "Nasal flaring",
                "Chest indrawing",
            ],
            "severity": RiskLevel.HIGH,
            "triage_color": TriageSeverity.RED,
            "recommended_action": "🔴 EMERGENCY! Go to hospital immediately. May indicate respiratory distress.",
            "facility_level": FacilityLevel.SECONDARY,
            "urgency": "immediate",
            "home_care_instructions": "Keep baby in comfortable position. Keep warm. Go to hospital.",
        },
        {
            "sign_name": "Severe chest indrawing",
            "description": "Lower chest drawing in during breathing",
            "symptoms": ["Chest pulls in", "Difficulty breathing", "Grunting"],
            "severity": RiskLevel.HIGH,
            "triage_color": TriageSeverity.RED,
            "recommended_action": "🔴 EMERGENCY! Go to hospital immediately. Sign of severe respiratory infection.",
            "facility_level": FacilityLevel.SECONDARY,
            "urgency": "immediate",
            "home_care_instructions": "Keep baby upright. Keep warm. Go to hospital.",
        },
        {
            "sign_name": "Fever (≥37.5°C)",
            "description": "Elevated temperature in newborn",
            "symptoms": ["Hot body", "Warm to touch", "Flushed", "Sweating"],
            "severity": RiskLevel.HIGH,
            "triage_color": TriageSeverity.RED,
            "recommended_action": "🔴 EMERGENCY! Go to health center IMMEDIATELY. Fever in newborn is serious.",
            "facility_level": FacilityLevel.PRIMARY,
            "urgency": "immediate",
            "home_care_instructions": "Undress baby lightly. Keep room warm but not hot. Go to hospital.",
        },
        {
            "sign_name": "Low temperature (<35.5°C)",
            "description": "Body temperature too low (hypothermia)",
            "symptoms": ["Cold body", "Cold extremities", "Lethargy", "Weak cry"],
            "severity": RiskLevel.HIGH,
            "triage_color": TriageSeverity.RED,
            "recommended_action": "🔴 EMERGENCY! Go to health center IMMEDIATELY. Hypothermia is dangerous.",
            "facility_level": FacilityLevel.PRIMARY,
            "urgency": "immediate",
            "home_care_instructions": "Skin-to-skin contact. Wrap baby with blanket. Keep head covered. Warm room.",
        },
        {
            "sign_name": "Yellow palms and soles",
            "description": "Jaundice extending to palms and soles - severe jaundice",
            "symptoms": [
                "Yellow skin",
                "Yellow eyes",
                "Yellow palms",
                "Yellow soles",
                "Lethargy",
            ],
            "severity": RiskLevel.HIGH,
            "triage_color": TriageSeverity.RED,
            "recommended_action": "🔴 EMERGENCY! Go to hospital. Severe jaundice needs treatment.",
            "facility_level": FacilityLevel.SECONDARY,
            "urgency": "same_day",
            "home_care_instructions": "Feed frequently to help bilirubin exit body. Do not expose to direct sunlight.",
        },
        {
            "sign_name": "Lethargy or unconsciousness",
            "description": "Baby unusually drowsy, difficult to wake, or unconscious",
            "symptoms": ["Difficult to wake", "Unconscious", "Floppy", "Unresponsive"],
            "severity": RiskLevel.CRITICAL,
            "triage_color": TriageSeverity.RED,
            "recommended_action": "🔴 EXTREME EMERGENCY! Go to hospital IMMEDIATELY.",
            "facility_level": FacilityLevel.TERTIARY,
            "urgency": "immediate",
            "home_care_instructions": "Keep baby warm. Go to hospital immediately.",
        },
        {
            "sign_name": "Umbilical cord infection",
            "description": "Redness, swelling, or pus at umbilical cord stump",
            "symptoms": [
                "Redness around cord",
                "Swelling",
                "Pus",
                "Foul smell",
                "Bleeding",
            ],
            "severity": RiskLevel.MEDIUM,
            "triage_color": TriageSeverity.YELLOW,
            "recommended_action": "🟡 Visit health center TODAY. May need antibiotics.",
            "facility_level": FacilityLevel.PRIMARY,
            "urgency": "within_24h",
            "home_care_instructions": "Keep cord clean and dry. Do not cover with bandage. Fold diaper below cord.",
        },
    ]

    # ============ INFANT DANGER SIGNS (1-12 months) - IMCI ============

    INFANT_DANGER_SIGNS = [
        {
            "sign_name": "Unable to drink or breastfeed",
            "description": "Child unable to take fluids",
            "symptoms": ["Refusing fluids", "Unable to suck", "Vomiting everything"],
            "severity": RiskLevel.CRITICAL,
            "triage_color": TriageSeverity.RED,
            "recommended_action": "🔴 EMERGENCY! Go to hospital IMMEDIATELY. Risk of dehydration.",
            "facility_level": FacilityLevel.SECONDARY,
            "urgency": "immediate",
            "home_care_instructions": "Try giving small sips of ORS (oral rehydration solution) frequently.",
        },
        {
            "sign_name": "Convulsions",
            "description": "Child having seizures",
            "symptoms": ["Jerking movements", "Stiffening", "Unconsciousness"],
            "severity": RiskLevel.CRITICAL,
            "triage_color": TriageSeverity.RED,
            "recommended_action": "🔴 EMERGENCY! Go to hospital IMMEDIATELY.",
            "facility_level": FacilityLevel.TERTIARY,
            "urgency": "immediate",
            "home_care_instructions": "Place child on side. Do not put anything in mouth. Go to hospital.",
        },
        {
            "sign_name": "Fast breathing (≥50/min for 2-12 months)",
            "description": "Breathing rate 50+ breaths per minute",
            "symptoms": [
                "Rapid breathing",
                "Grunting",
                "Chest indrawing",
                "Nasal flaring",
            ],
            "severity": RiskLevel.HIGH,
            "triage_color": TriageSeverity.RED,
            "recommended_action": "🔴 EMERGENCY! Go to hospital. Possible pneumonia.",
            "facility_level": FacilityLevel.SECONDARY,
            "urgency": "immediate",
            "home_care_instructions": "Keep child comfortable. Continue feeding. Go to hospital.",
        },
        {
            "sign_name": "Severe chest indrawing",
            "description": "Lower chest drawing in during breathing",
            "symptoms": ["Chest pulls in", "Difficulty breathing", "Grunting"],
            "severity": RiskLevel.HIGH,
            "triage_color": TriageSeverity.RED,
            "recommended_action": "🔴 EMERGENCY! Go to hospital. Possible severe pneumonia.",
            "facility_level": FacilityLevel.SECONDARY,
            "urgency": "immediate",
            "home_care_instructions": "Keep child upright. Continue fluids. Go to hospital.",
        },
        {
            "sign_name": "Persistent vomiting",
            "description": "Vomiting everything, unable to keep fluids down",
            "symptoms": [
                "Repeated vomiting",
                "Unable to keep fluids",
                "Signs of dehydration",
            ],
            "severity": RiskLevel.HIGH,
            "triage_color": TriageSeverity.YELLOW,
            "recommended_action": "🟡 Visit health center TODAY. Risk of dehydration.",
            "facility_level": FacilityLevel.PRIMARY,
            "urgency": "same_day",
            "home_care_instructions": "Give small sips frequently. ORS solution. Watch for dehydration signs.",
        },
        {
            "sign_name": "Diarrhea with blood",
            "description": "Bloody diarrhea (dysentery)",
            "symptoms": [
                "Blood in stool",
                "Frequent loose stools",
                "Fever",
                "Abdominal pain",
            ],
            "severity": RiskLevel.HIGH,
            "triage_color": TriageSeverity.YELLOW,
            "recommended_action": "🟡 Visit health center TODAY. Needs antibiotics.",
            "facility_level": FacilityLevel.PRIMARY,
            "urgency": "same_day",
            "home_care_instructions": "Give ORS frequently. Continue feeding. Do not give anti-diarrheal medications.",
        },
        {
            "sign_name": "High fever",
            "description": "Temperature above 38.5°C",
            "symptoms": ["High temperature", "Hot body", "Irritability"],
            "severity": RiskLevel.MEDIUM,
            "triage_color": TriageSeverity.YELLOW,
            "recommended_action": "🟡 Visit health center TODAY. Fever needs evaluation.",
            "facility_level": FacilityLevel.PRIMARY,
            "urgency": "within_24h",
            "home_care_instructions": "Give paracetamol. Dress lightly. Give fluids. Monitor temperature.",
        },
    ]

    # ============ CHILD UNDER-5 DANGER SIGNS - IMCI ============

    CHILD_DANGER_SIGNS = {
        ChildAgeGroup.TODDLER: [  # 1-3 years
            {
                "sign_name": "Unable to drink",
                "description": "Child unable or unwilling to drink",
                "symptoms": [
                    "Refusing fluids",
                    "Lethargy",
                    "Dry mouth",
                    "No tears when crying",
                ],
                "severity": RiskLevel.CRITICAL,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital IMMEDIATELY. Severe dehydration risk.",
                "facility_level": FacilityLevel.SECONDARY,
                "urgency": "immediate",
                "home_care_instructions": "Try small sips of ORS. Ice chips. Seek medical help.",
            },
            {
                "sign_name": "Convulsions",
                "description": "Seizures or fits",
                "symptoms": ["Jerking", "Stiffening", "Unconsciousness", "Eye rolling"],
                "severity": RiskLevel.CRITICAL,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital IMMEDIATELY.",
                "facility_level": FacilityLevel.TERTIARY,
                "urgency": "immediate",
                "home_care_instructions": "Place on side. Do not restrain. Do not put anything in mouth. Go to hospital.",
            },
            {
                "sign_name": "Fast breathing (≥40/min)",
                "description": "Breathing rate 40+ breaths per minute (1-5 years)",
                "symptoms": [
                    "Rapid breathing",
                    "Chest indrawing",
                    "Grunting",
                    "Difficulty breathing",
                ],
                "severity": RiskLevel.HIGH,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital. Possible severe pneumonia.",
                "facility_level": FacilityLevel.SECONDARY,
                "urgency": "immediate",
                "home_care_instructions": "Keep child comfortable. Continue fluids. Go to hospital.",
            },
            {
                "sign_name": "Severe malnutrition signs",
                "description": "Visible severe wasting, edema, or skin changes",
                "symptoms": [
                    "Very thin arms/legs",
                    "Swollen belly",
                    "Swollen feet",
                    "Skin changes",
                    "Hair changes",
                ],
                "severity": RiskLevel.HIGH,
                "triage_color": TriageSeverity.YELLOW,
                "recommended_action": "🟡 Visit health center TODAY for nutritional assessment.",
                "facility_level": FacilityLevel.PRIMARY,
                "urgency": "same_day",
                "home_care_instructions": "Continue feeding frequent small meals. High-energy foods.",
            },
            {
                "sign_name": "Lethargy or unconsciousness",
                "description": "Child unusually drowsy, difficult to wake, or unconscious",
                "symptoms": [
                    "Difficult to wake",
                    "Unconscious",
                    "Floppy",
                    "Unresponsive",
                ],
                "severity": RiskLevel.CRITICAL,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital IMMEDIATELY.",
                "facility_level": FacilityLevel.TERTIARY,
                "urgency": "immediate",
                "home_care_instructions": "Keep child on side. Keep warm. Go to hospital immediately.",
            },
            {
                "sign_name": "Persistent vomiting",
                "description": "Vomiting everything",
                "symptoms": ["Repeated vomiting", "Unable to keep fluids"],
                "severity": RiskLevel.HIGH,
                "triage_color": TriageSeverity.YELLOW,
                "recommended_action": "🟡 Visit health center TODAY. Risk of dehydration.",
                "facility_level": FacilityLevel.PRIMARY,
                "urgency": "same_day",
                "home_care_instructions": "Give small sips of ORS frequently.",
            },
        ],
        ChildAgeGroup.PRESCHOOL: [  # 3-5 years
            {
                "sign_name": "Unable to drink",
                "description": "Child unable or unwilling to drink",
                "symptoms": ["Refusing fluids", "Lethargy", "Dehydration signs"],
                "severity": RiskLevel.CRITICAL,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital IMMEDIATELY.",
                "facility_level": FacilityLevel.SECONDARY,
                "urgency": "immediate",
                "home_care_instructions": "Offer small sips frequently. ORS. Ice chips. Seek medical help.",
            },
            {
                "sign_name": "Convulsions",
                "description": "Seizures",
                "symptoms": [
                    "Jerking movements",
                    "Stiffening",
                    "Loss of consciousness",
                ],
                "severity": RiskLevel.CRITICAL,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital IMMEDIATELY.",
                "facility_level": FacilityLevel.TERTIARY,
                "urgency": "immediate",
                "home_care_instructions": "Place on side. Clear area. Do not restrain. Go to hospital.",
            },
            {
                "sign_name": "Fast breathing (≥40/min)",
                "description": "Breathing rate 40+ breaths per minute",
                "symptoms": [
                    "Rapid breathing",
                    "Chest indrawing",
                    "Difficulty breathing",
                ],
                "severity": RiskLevel.HIGH,
                "triage_color": TriageSeverity.RED,
                "recommended_action": "🔴 EMERGENCY! Go to hospital for evaluation.",
                "facility_level": FacilityLevel.SECONDARY,
                "urgency": "immediate",
                "home_care_instructions": "Keep comfortable. Continue fluids. Go to hospital.",
            },
            {
                "sign_name": "Severe paleness",
                "description": "Very pale palms, conjunctiva, or nail beds - sign of severe anemia",
                "symptoms": [
                    "Pale palms",
                    "Pale inner eyelids",
                    "Pale nail beds",
                    "Weakness",
                    "Fatigue",
                ],
                "severity": RiskLevel.HIGH,
                "triage_color": TriageSeverity.YELLOW,
                "recommended_action": "🟡 Visit health center for blood test and treatment.",
                "facility_level": FacilityLevel.PRIMARY,
                "urgency": "same_day",
                "home_care_instructions": "Iron-rich foods: dark leafy greens, beans, meat. Vitamin C to help absorption.",
            },
            {
                "sign_name": "Swollen abdomen with edema",
                "description": "Distended belly with swelling of feet - kwashiorkor",
                "symptoms": [
                    "Swollen belly",
                    "Swollen feet",
                    "Skin changes",
                    "Hair changes",
                    "Irritability",
                ],
                "severity": RiskLevel.HIGH,
                "triage_color": TriageSeverity.YELLOW,
                "recommended_action": "🟡 Visit health center for nutritional rehabilitation.",
                "facility_level": FacilityLevel.PRIMARY,
                "urgency": "same_day",
                "home_care_instructions": "Continue feeding. Small frequent meals. Protein-rich foods when available.",
            },
        ],
    }

    # ============ ADOLESCENT DANGER SIGNS (10-19 years) ============

    ADOLESCENT_DANGER_SIGNS = [
        # Mental Health
        {
            "sign_name": "Thoughts of self-harm or suicide",
            "description": "Expressing thoughts of wanting to die or harm themselves",
            "symptoms": [
                "Talking about death",
                "Self-harm",
                "Withdrawal",
                "Hopelessness",
            ],
            "severity": RiskLevel.CRITICAL,
            "triage_color": TriageSeverity.RED,
            "recommended_action": "🔴 EMERGENCY! Seek immediate help from healthcare provider or counselor.",
            "facility_level": FacilityLevel.SECONDARY,
            "urgency": "immediate",
            "home_care_instructions": "Do not leave alone. Listen without judgment. Get help immediately.",
        },
        {
            "sign_name": "Severe depression or anxiety",
            "description": "Persistent sadness, anxiety, or mood changes",
            "symptoms": [
                "Sadness >2 weeks",
                "Loss of interest",
                "Sleep problems",
                "Appetite changes",
            ],
            "severity": RiskLevel.HIGH,
            "triage_color": TriageSeverity.YELLOW,
            "recommended_action": "🟡 Visit health center THIS WEEK. Mental health support available.",
            "facility_level": FacilityLevel.PRIMARY,
            "urgency": "within_24h",
            "home_care_instructions": "Talk to trusted adult. Stay active. Maintain social connections.",
        },
        # Reproductive Health
        {
            "sign_name": "Severe abdominal pain (possible pregnancy complication)",
            "description": "Severe lower abdominal pain in sexually active adolescent",
            "symptoms": ["Severe pain", "Bleeding", "Dizziness", "Fainting"],
            "severity": RiskLevel.HIGH,
            "triage_color": TriageSeverity.RED,
            "recommended_action": "🔴 EMERGENCY! Go to hospital immediately. Could be ectopic pregnancy.",
            "facility_level": FacilityLevel.SECONDARY,
            "urgency": "immediate",
            "home_care_instructions": "Lie down. Have someone accompany you to hospital.",
        },
        {
            "sign_name": "Abnormal vaginal bleeding",
            "description": "Very heavy or prolonged menstrual bleeding",
            "symptoms": [
                "Soaking pad every hour",
                "Bleeding >7 days",
                "Large clots",
                "Dizziness",
            ],
            "severity": RiskLevel.MEDIUM,
            "triage_color": TriageSeverity.YELLOW,
            "recommended_action": "🟡 Visit health center THIS WEEK. Needs evaluation.",
            "facility_level": FacilityLevel.PRIMARY,
            "urgency": "within_24h",
            "home_care_instructions": "Rest. Drink iron-rich fluids. Monitor bleeding.",
        },
        # Substance Use
        {
            "sign_name": "Signs of substance overdose",
            "description": "Unconsciousness or difficulty breathing after substance use",
            "symptoms": ["Unconsciousness", "Slow breathing", "Confusion", "Vomiting"],
            "severity": RiskLevel.CRITICAL,
            "triage_color": TriageSeverity.RED,
            "recommended_action": "🔴 EMERGENCY! Call emergency services IMMEDIATELY.",
            "facility_level": FacilityLevel.TERTIARY,
            "urgency": "immediate",
            "home_care_instructions": "Place on side. Do not leave alone. Call emergency.",
        },
        # General
        {
            "sign_name": "Severe headache with vision changes",
            "description": "Severe headache with blurred vision or confusion",
            "symptoms": ["Severe headache", "Blurred vision", "Confusion", "Vomiting"],
            "severity": RiskLevel.HIGH,
            "triage_color": TriageSeverity.RED,
            "recommended_action": "🔴 EMERGENCY! Go to hospital immediately.",
            "facility_level": FacilityLevel.SECONDARY,
            "urgency": "immediate",
            "home_care_instructions": "Rest. Do not drive. Have someone take you to hospital.",
        },
        {
            "sign_name": "Difficulty breathing",
            "description": "Shortness of breath or difficulty breathing",
            "symptoms": ["Shortness of breath", "Rapid breathing", "Chest pain"],
            "severity": RiskLevel.HIGH,
            "triage_color": TriageSeverity.RED,
            "recommended_action": "🔴 EMERGENCY! Go to hospital immediately.",
            "facility_level": FacilityLevel.SECONDARY,
            "urgency": "immediate",
            "home_care_instructions": "Sit upright. Stay calm. Go to hospital.",
        },
        {
            "sign_name": "Mild menstrual cramps",
            "description": "Common menstrual pain",
            "symptoms": ["Mild cramps", "Bloating", "Mood changes"],
            "severity": RiskLevel.LOW,
            "triage_color": TriageSeverity.GREEN,
            "recommended_action": "🟢 HOME CARE is safe.",
            "facility_level": FacilityLevel.PRIMARY,
            "urgency": "monitor",
            "home_care_instructions": "Use hot water bottle. Take paracetamol. Rest. Exercise lightly.",
        },
    ]

    @classmethod
    def get_maternal_danger_signs(cls, stage: PregnancyStage) -> List[Dict]:
        """Get danger signs for specific pregnancy stage"""
        return cls.MATERNAL_DANGER_SIGNS.get(stage, [])

    @classmethod
    def get_all_maternal_danger_signs(cls) -> List[Dict]:
        """Get all maternal danger signs across all stages"""
        all_signs = []
        for stage_signs in cls.MATERNAL_DANGER_SIGNS.values():
            all_signs.extend(stage_signs)
        return all_signs

    @classmethod
    def get_neonatal_danger_signs(cls) -> List[Dict]:
        """Get all neonatal danger signs (0-28 days)"""
        return cls.NEONATAL_DANGER_SIGNS

    @classmethod
    def get_infant_danger_signs(cls) -> List[Dict]:
        """Get all infant danger signs (1-12 months)"""
        return cls.INFANT_DANGER_SIGNS

    @classmethod
    def get_child_danger_signs(cls, age_group: ChildAgeGroup) -> List[Dict]:
        """Get danger signs for specific child age group"""
        return cls.CHILD_DANGER_SIGNS.get(age_group, [])

    @classmethod
    def get_all_child_danger_signs(cls) -> List[Dict]:
        """Get all child danger signs across all age groups"""
        all_signs = []
        for age_signs in cls.CHILD_DANGER_SIGNS.values():
            all_signs.extend(age_signs)
        return all_signs

    @classmethod
    def get_adolescent_danger_signs(cls) -> List[Dict]:
        """Get all adolescent danger signs (10-19 years)"""
        return cls.ADOLESCENT_DANGER_SIGNS

    @classmethod
    def search_danger_signs(cls, query: str, patient_type: str = None) -> List[Dict]:
        """Search danger signs by symptom or sign name"""
        results = []
        query_lower = query.lower()

        # Build search pool based on patient type
        all_signs = []

        if patient_type == "mother" or not patient_type:
            all_signs.extend(cls.get_all_maternal_danger_signs())
        if patient_type == "neonate" or not patient_type:
            all_signs.extend(cls.get_neonatal_danger_signs())
        if patient_type == "infant" or not patient_type:
            all_signs.extend(cls.get_infant_danger_signs())
        if patient_type == "child" or not patient_type:
            all_signs.extend(cls.get_all_child_danger_signs())
        if patient_type == "adolescent" or not patient_type:
            all_signs.extend(cls.get_adolescent_danger_signs())

        for sign in all_signs:
            if (
                query_lower in sign["sign_name"].lower()
                or query_lower in sign["description"].lower()
                or any(
                    query_lower in symptom.lower()
                    for symptom in sign.get("symptoms", [])
                )
            ):
                results.append(sign)

        return results

    @classmethod
    def get_emergency_danger_signs(cls, patient_type: str = None) -> List[Dict]:
        """Get all danger signs requiring immediate action (RED)"""
        all_signs = []

        if patient_type == "mother" or not patient_type:
            all_signs.extend(cls.get_all_maternal_danger_signs())
        if patient_type == "neonate" or not patient_type:
            all_signs.extend(cls.get_neonatal_danger_signs())
        if patient_type == "infant" or not patient_type:
            all_signs.extend(cls.get_infant_danger_signs())
        if patient_type == "child" or not patient_type:
            all_signs.extend(cls.get_all_child_danger_signs())
        if patient_type == "adolescent" or not patient_type:
            all_signs.extend(cls.get_adolescent_danger_signs())

        return [
            sign for sign in all_signs if sign.get("triage_color") == TriageSeverity.RED
        ]

    @classmethod
    def get_triage_summary(cls, patient_type: str = None) -> Dict:
        """Get summary count by triage color"""
        all_signs = []

        if patient_type == "mother":
            all_signs.extend(cls.get_all_maternal_danger_signs())
        elif patient_type == "neonate":
            all_signs.extend(cls.get_neonatal_danger_signs())
        elif patient_type == "infant":
            all_signs.extend(cls.get_infant_danger_signs())
        elif patient_type == "child":
            all_signs.extend(cls.get_all_child_danger_signs())
        elif patient_type == "adolescent":
            all_signs.extend(cls.get_adolescent_danger_signs())

        return {
            "red": len(
                [s for s in all_signs if s.get("triage_color") == TriageSeverity.RED]
            ),
            "yellow": len(
                [s for s in all_signs if s.get("triage_color") == TriageSeverity.YELLOW]
            ),
            "green": len(
                [s for s in all_signs if s.get("triage_color") == TriageSeverity.GREEN]
            ),
            "total": len(all_signs),
        }
