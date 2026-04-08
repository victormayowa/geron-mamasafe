"""
Risk Stratification Service
Assesses and categorizes risk levels for mothers and children
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, date

from app.models.models import (
    Mother, Child, RiskLevel, PregnancyStage,
    ChildAgeGroup, Alert
)

logger = logging.getLogger(__name__)


class RiskStratificationService:
    """Service for assessing and managing risk levels"""

    # High-risk pregnancy conditions
    HIGH_RISK_CONDITIONS = [
        "preeclampsia", "eclampsia", "gestational diabetes", "placenta previa",
        "placental abruption", "ectopic pregnancy", "multiple pregnancy",
        "previous c-section", "rh negative", "hiv positive", "hepatitis b",
        "tuberculosis", "malaria", "severe anemia", "heart disease",
        "kidney disease", "hypertension", "diabetes"
    ]

    # High-risk factors for mothers
    MATERNAL_RISK_FACTORS = {
        "age_below_18": {"weight": 2, "description": "Age below 18 years"},
        "age_above_35": {"weight": 2, "description": "Age above 35 years"},
        "first_pregnancy": {"weight": 1, "description": "First pregnancy (primigravida)"},
        "high_parity": {"weight": 2, "description": "High parity (5+ births)"},
        "previous_stillbirth": {"weight": 3, "description": "Previous stillbirth or neonatal death"},
        "previous_c_section": {"weight": 2, "description": "Previous cesarean section"},
        "previous_complications": {"weight": 3, "description": "Previous pregnancy complications"},
        "chronic_hypertension": {"weight": 3, "description": "Chronic hypertension"},
        "diabetes": {"weight": 3, "description": "Pre-existing diabetes"},
        "heart_disease": {"weight": 3, "description": "Heart disease"},
        "kidney_disease": {"weight": 3, "description": "Kidney disease"},
        "hiv_positive": {"weight": 2, "description": "HIV positive"},
        "severe_anemia": {"weight": 3, "description": "Severe anemia (Hb < 7g/dL)"},
        "multiple_pregnancy": {"weight": 3, "description": "Twins or multiples"},
        "rh_negative": {"weight": 2, "description": "Rh-negative blood group"},
        "short_stature": {"weight": 1, "description": "Short stature (<150cm)"},
        "underweight": {"weight": 1, "description": "Underweight (BMI < 18.5)"},
        "obese": {"weight": 2, "description": "Obese (BMI ≥ 30)"},
        "substance_abuse": {"weight": 3, "description": "Substance abuse"},
        "domestic_violence": {"weight": 3, "description": "Domestic violence"}
    }

    # High-risk factors for children
    CHILD_RISK_FACTORS = {
        "low_birth_weight": {"weight": 3, "description": "Low birth weight (<2.5kg)"},
        "very_low_birth_weight": {"weight": 4, "description": "Very low birth weight (<1.5kg)"},
        "preterm_birth": {"weight": 3, "description": "Preterm birth (<37 weeks)"},
        "post_term_birth": {"weight": 2, "description": "Post-term birth (>42 weeks)"},
        "birth_asphyxia": {"weight": 4, "description": "Birth asphyxia (low Apgar score)"},
        "congenital_anomalies": {"weight": 3, "description": "Congenital anomalies"},
        "twins_multiples": {"weight": 2, "description": "Twins or multiples"},
        "not_breastfeeding": {"weight": 2, "description": "Not breastfeeding"},
        "malnutrition": {"weight": 3, "description": "Malnutrition"},
        "incomplete_immunization": {"weight": 2, "description": "Incomplete immunization"},
        "recurrent_infections": {"weight": 2, "description": "Recurrent infections"},
        "mother_hiv_positive": {"weight": 2, "description": "Mother HIV positive"}
    }

    async def assess_mother_risk(self, mother: Mother) -> Tuple[RiskLevel, List[str], str]:
        """
        Assess risk level for a mother
        
        Args:
            mother: Mother object
            
        Returns:
            Tuple of (risk_level, risk_factors_list, risk_factors_description)
        """
        risk_score = 0
        identified_risks = []

        # Age-related risks
        if mother.age:
            if mother.age < 18:
                risk_score += self.MATERNAL_RISK_FACTORS["age_below_18"]["weight"]
                identified_risks.append(self.MATERNAL_RISK_FACTORS["age_below_18"]["description"])
            elif mother.age > 35:
                risk_score += self.MATERNAL_RISK_FACTORS["age_above_35"]["weight"]
                identified_risks.append(self.MATERNAL_RISK_FACTORS["age_above_35"]["description"])

        # Pregnancy history risks
        if mother.gravida is not None:
            if mother.gravida == 1:
                risk_score += self.MATERNAL_RISK_FACTORS["first_pregnancy"]["weight"]
                identified_risks.append(self.MATERNAL_RISK_FACTORS["first_pregnancy"]["description"])
        
        if mother.parity is not None and mother.parity >= 5:
            risk_score += self.MATERNAL_RISK_FACTORS["high_parity"]["weight"]
            identified_risks.append(self.MATERNAL_RISK_FACTORS["high_parity"]["description"])

        # Previous complications
        if mother.previous_complications:
            risk_score += self.MATERNAL_RISK_FACTORS["previous_complications"]["weight"]
            identified_risks.append(self.MATERNAL_RISK_FACTORS["previous_complications"]["description"])

        # Chronic conditions
        if mother.chronic_conditions:
            conditions = mother.chronic_conditions.lower()
            for condition in self.HIGH_RISK_CONDITIONS:
                if condition in conditions:
                    risk_score += 3
                    identified_risks.append(f"Chronic condition: {condition}")

        # Blood group risks
        if mother.blood_group and "rh" in mother.blood_group.lower():
            risk_score += self.MATERNAL_RISK_FACTORS["rh_negative"]["weight"]
            identified_risks.append(self.MATERNAL_RISK_FACTORS["rh_negative"]["description"])

        # Pregnancy stage risks (third trimester is higher risk)
        if mother.pregnancy_stage == PregnancyStage.THIRD_TRIMESTER:
            risk_score += 1
            identified_risks.append("Third trimester - increased monitoring needed")

        # Determine risk level
        risk_level = self._calculate_risk_level(risk_score)

        # Check if high risk
        is_high_risk = risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]

        # Update mother's risk assessment
        mother.risk_level = risk_level
        mother.is_high_risk = is_high_risk
        mother.risk_factors = ", ".join(identified_risks) if identified_risks else None

        return risk_level, identified_risks, ", ".join(identified_risks) if identified_risks else "No significant risk factors identified"

    async def assess_child_risk(self, child: Child, mother: Optional[Mother] = None) -> Tuple[RiskLevel, List[str], str]:
        """
        Assess risk level for a child
        
        Args:
            child: Child object
            mother: Optional mother object for additional context
            
        Returns:
            Tuple of (risk_level, risk_factors_list, risk_factors_description)
        """
        risk_score = 0
        identified_risks = []

        # Birth weight risks
        if child.birth_weight is not None:
            if child.birth_weight < 1.5:
                risk_score += self.CHILD_RISK_FACTORS["very_low_birth_weight"]["weight"]
                identified_risks.append(self.CHILD_RISK_FACTORS["very_low_birth_weight"]["description"])
            elif child.birth_weight < 2.5:
                risk_score += self.CHILD_RISK_FACTORS["low_birth_weight"]["weight"]
                identified_risks.append(self.CHILD_RISK_FACTORS["low_birth_weight"]["description"])

        # Gestational age risks
        if child.gestational_age is not None:
            if child.gestational_age < 37:
                risk_score += self.CHILD_RISK_FACTORS["preterm_birth"]["weight"]
                identified_risks.append(self.CHILD_RISK_FACTORS["preterm_birth"]["description"])
            elif child.gestational_age > 42:
                risk_score += self.CHILD_RISK_FACTORS["post_term_birth"]["weight"]
                identified_risks.append(self.CHILD_RISK_FACTORS["post_term_birth"]["description"])

        # Birth complications
        if child.apgar_score is not None and child.apgar_score < 7:
            risk_score += self.CHILD_RISK_FACTORS["birth_asphyxia"]["weight"]
            identified_risks.append(self.CHILD_RISK_FACTORS["birth_asphyxia"]["description"])

        if child.complications_at_birth:
            risk_score += 2
            identified_risks.append(f"Birth complications: {child.complications_at_birth}")

        # Feeding risks
        if child.feeding_method and child.feeding_method.lower() not in ["breastfeeding", "breast milk"]:
            if child.age_group in [ChildAgeGroup.NEWBORN, ChildAgeGroup.INFANT]:
                risk_score += self.CHILD_RISK_FACTORS["not_breastfeeding"]["weight"]
                identified_risks.append(self.CHILD_RISK_FACTORS["not_breastfeeding"]["description"])

        # Current health status
        if child.current_weight is not None and child.birth_weight is not None:
            # Check for poor weight gain
            weight_gain = child.current_weight - child.birth_weight
            if weight_gain < 0.5:  # Less than 500g gain
                risk_score += self.CHILD_RISK_FACTORS["malnutrition"]["weight"]
                identified_risks.append("Poor weight gain detected")

        # Mother's health status
        if mother and mother.is_high_risk:
            risk_score += 2
            identified_risks.append("High-risk mother")

        if mother and mother.chronic_conditions:
            if "hiv" in mother.chronic_conditions.lower():
                risk_score += self.CHILD_RISK_FACTORS["mother_hiv_positive"]["weight"]
                identified_risks.append("Mother HIV positive")

        # Determine risk level
        risk_level = self._calculate_risk_level(risk_score)

        # Check if high risk
        is_high_risk = risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]

        # Update child's risk assessment
        child.risk_level = risk_level
        child.is_high_risk = is_high_risk
        child.risk_factors = ", ".join(identified_risks) if identified_risks else None

        return risk_level, identified_risks, ", ".join(identified_risks) if identified_risks else "No significant risk factors identified"

    def _calculate_risk_level(self, risk_score: int) -> RiskLevel:
        """
        Calculate risk level based on risk score
        
        Args:
            risk_score: Total risk score
            
        Returns:
            RiskLevel enum
        """
        if risk_score >= 8:
            return RiskLevel.CRITICAL
        elif risk_score >= 5:
            return RiskLevel.HIGH
        elif risk_score >= 2:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW

    async def create_risk_alert(self, mother: Optional[Mother], child: Optional[Child], 
                                risk_level: RiskLevel, risk_description: str) -> Alert:
        """
        Create an alert for high-risk mother or child
        
        Args:
            mother: Mother object (optional)
            child: Child object (optional)
            risk_level: Risk level
            risk_description: Description of risk factors
            
        Returns:
            Created Alert object
        """
        alert = Alert(
            mother_id=mother.id if mother else None,
            child_id=child.id if child else None,
            alert_type="high_risk",
            title=f"High Risk Alert - {risk_level.value.upper()}",
            description=risk_description,
            severity=risk_level,
            is_resolved=False,
            notification_sent=False
        )
        
        return alert

    @staticmethod
    def get_risk_recommendations(risk_level: RiskLevel, is_mother: bool = True) -> str:
        """
        Get recommendations based on risk level
        
        Args:
            risk_level: Risk level
            is_mother: Whether this is for a mother (True) or child (False)
            
        Returns:
            Recommendations string
        """
        subject = "mother" if is_mother else "child"
        
        recommendations = {
            RiskLevel.LOW: f"✅ Low Risk\n\nContinue regular check-ups and maintain healthy practices.",
            
            RiskLevel.MEDIUM: f"⚡ Medium Risk\n\n• Increase monitoring frequency\n• Attend all scheduled appointments\n• Report any unusual symptoms immediately\n• Follow healthcare provider's advice",
            
            RiskLevel.HIGH: f"⚠️ HIGH RISK\n\n• Requires close medical supervision\n• Frequent check-ups needed\n• Know the danger signs\n• Have transport plan to secondary/tertiary facility\n• Keep emergency contacts readily available\n• Do not delay seeking care",
            
            RiskLevel.CRITICAL: f"🚨 CRITICAL RISK - IMMEDIATE ATTENTION NEEDED\n\n• Requires immediate medical evaluation\n• May need referral to secondary/tertiary facility\n• Continuous monitoring essential\n• Have emergency transport arranged\n• Do not wait for symptoms to worsen\n• Seek specialized care immediately"
        }
        
        return recommendations.get(risk_level, "Risk level not determined")
