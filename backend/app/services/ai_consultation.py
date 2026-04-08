"""
AI Consultation Service - FREE LLM Options
Supports: Groq (free tier), Ollama (local), HuggingFace (free), OpenAI (paid)
Combines rule-based medical knowledge with LLM capabilities
"""

import json
import logging
import httpx
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from groq import AsyncGroq
from openai import AsyncOpenAI
import ollama
from huggingface_hub import AsyncInferenceClient

from app.core.config import settings
from app.services.danger_signs_db import DangerSignsDatabase
from app.models.models import RiskLevel, PregnancyStage, ChildAgeGroup, TriageSeverity

logger = logging.getLogger(__name__)


class AIConsultationService:
    """AI service for handling health consultations with FREE LLM options"""

    def __init__(self):
        self.groq_client = None
        self.openai_client = None
        self.huggingface_client = None

        # Initialize Groq (Free tier - Recommended)
        if settings.GROQ_API_KEY:
            self.groq_client = AsyncGroq(api_key=settings.GROQ_API_KEY)

        # Initialize OpenAI (Paid)
        if settings.OPENAI_API_KEY:
            self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        # Initialize HuggingFace (Free tier)
        if settings.HUGGINGFACE_API_KEY:
            self.huggingface_client = AsyncInferenceClient(
                model=settings.HUGGINGFACE_MODEL, token=settings.HUGGINGFACE_API_KEY
            )

    async def process_query(
        self,
        query: str,
        patient_type: str = "mother",
        patient_profile: Optional[Dict] = None,
    ) -> Dict:
        """
        Process a health-related query and return intelligent response

        Args:
            query: User's question or symptom description
            patient_type: mother, neonate, infant, child, adolescent
            patient_profile: Patient's health profile (optional)

        Returns:
            Dictionary with response, triage level, and recommendations
        """

        # Step 1: Check for danger signs (Rule-based first)
        danger_sign_match = self._check_danger_signs(query, patient_type)

        if danger_sign_match:
            return self._format_danger_sign_response(danger_sign_match, patient_profile)

        # Step 2: Categorize the query
        category = self._categorize_query(query)

        # Step 3: Generate response using FREE LLM
        if category in ["danger_signs", "symptoms", "emergency"]:
            response = await self._generate_medical_response(
                query, patient_type, patient_profile
            )
            triage = self._assess_triage(query, response)
        else:
            response = await self._generate_general_response(
                query, patient_type, patient_profile
            )
            triage = TriageSeverity.GREEN

        return {
            "response": response,
            "category": category,
            "triage_severity": triage,
            "ai_confidence": 0.85,
            "requires_follow_up": triage in [TriageSeverity.YELLOW, TriageSeverity.RED],
            "escalated": triage == TriageSeverity.RED,
        }

    def _check_danger_signs(self, query: str, patient_type: str) -> Optional[Dict]:
        """Check if query matches any known danger signs"""
        results = DangerSignsDatabase.search_danger_signs(query, patient_type)

        if results:
            # Return highest severity match
            severity_order = {
                TriageSeverity.RED: 3,
                TriageSeverity.YELLOW: 2,
                TriageSeverity.GREEN: 1,
            }
            results_sorted = sorted(
                results,
                key=lambda x: severity_order.get(
                    x.get("triage_color", TriageSeverity.GREEN), 0
                ),
                reverse=True,
            )
            return results_sorted[0]

        return None

    def _format_danger_sign_response(
        self, danger_sign: Dict, patient_profile: Optional[Dict]
    ) -> Dict:
        """Format a danger sign match into a response (IMCI Traffic Light System)"""

        triage = danger_sign.get("triage_color", TriageSeverity.GREEN)

        if triage == TriageSeverity.RED:
            emoji = "🔴"
            urgency_text = "RED - EMERGENCY! GO TO HOSPITAL IMMEDIATELY"
        elif triage == TriageSeverity.YELLOW:
            emoji = "🟡"
            urgency_text = "YELLOW - VISIT HEALTH CENTER TODAY"
        else:
            emoji = "🟢"
            urgency_text = "GREEN - HOME CARE IS SAFE"

        response = f"""{emoji} {urgency_text}

⚕️ {danger_sign['sign_name']}

📋 What to look for:
{danger_sign['description']}

🔍 Common Symptoms:
{self._format_list(danger_sign.get('symptoms', []))}

✅ What You Should Do:
{danger_sign['recommended_action']}

🏥 Where to Go: {danger_sign['facility_level'].value.upper()}

⏰ When: {danger_sign.get('urgency', 'monitor')}"""

        if danger_sign.get("home_care_instructions"):
            response += f"""

🏠 Home Care Instructions:
{danger_sign['home_care_instructions']}"""

        return {
            "response": response,
            "category": "danger_signs",
            "triage_severity": triage,
            "ai_confidence": 0.95,
            "requires_follow_up": triage in [TriageSeverity.YELLOW, TriageSeverity.RED],
            "escalated": triage == TriageSeverity.RED,
            "danger_sign": danger_sign,
        }

    async def _generate_medical_response(
        self, query: str, patient_type: str, patient_profile: Optional[Dict]
    ) -> str:
        """Generate a medical response using FREE LLM"""

        system_prompt = self._build_medical_system_prompt(patient_type, patient_profile)

        # Try Groq first (Free tier, fast)
        if self.groq_client:
            try:
                response = await self.groq_client.chat.completions.create(
                    model=settings.GROQ_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": query},
                    ],
                    max_tokens=800,
                    temperature=0.3,
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.warning(f"Groq failed: {e}, trying next provider")

        # Try Ollama (Local, completely free)
        if settings.AI_PROVIDER == "ollama":
            try:
                response = await ollama.ChatAsync(
                    model=settings.OLLAMA_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": query},
                    ],
                )
                return response["message"]["content"]
            except Exception as e:
                logger.warning(f"Ollama failed: {e}, trying next provider")

        # Try HuggingFace (Free tier)
        if self.huggingface_client:
            try:
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query},
                ]
                response = await self.huggingface_client.chat_completion(
                    messages, max_tokens=800
                )
                return response[0]["generated_text"]
            except Exception as e:
                logger.warning(f"HuggingFace failed: {e}")

        # Fallback
        return self._get_fallback_response(query)

    async def _generate_general_response(
        self, query: str, patient_type: str, patient_profile: Optional[Dict]
    ) -> str:
        """Generate a general health education response using FREE LLM"""

        system_prompt = f"""You are a knowledgeable maternal, neonatal, and child health educator.
Provide helpful, evidence-based health education information in a warm, supportive tone.
Keep responses concise and easy to understand (WhatsApp-friendly).
Patient type: {patient_type}
Always encourage healthy practices and regular check-ups."""

        # Use same LLM priority: Groq > Ollama > HuggingFace
        if self.groq_client:
            try:
                response = await self.groq_client.chat.completions.create(
                    model=settings.GROQ_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": query},
                    ],
                    max_tokens=600,
                    temperature=0.7,
                )
                return response.choices[0].message.content
            except:
                pass

        return self._get_fallback_response(query)

    def _build_medical_system_prompt(
        self, patient_type: str, patient_profile: Optional[Dict]
    ) -> str:
        """Build system prompt for medical queries"""

        prompt = f"""You are an expert maternal, neonatal, child, and adolescent health AI assistant.
Patient Type: {patient_type.upper()}

Your role is to help understand health symptoms and know when to seek medical care.

IMPORTANT GUIDELINES:
1. Always prioritize safety - when in doubt, recommend seeking medical care
2. Use IMCI TRAFFIC LIGHT SYSTEM:
   - 🔴 RED = Emergency, go to hospital immediately
   - 🟡 YELLOW = Visit health center today
   - 🟢 GREEN = Home care is safe
3. Be clear about URGENCY levels
4. Specify which facility level to visit (Primary, Secondary, or Tertiary)
5. Provide home care instructions when appropriate
6. Use simple, clear language suitable for mothers/patients
7. Be empathetic and supportive
8. Never diagnose - only provide guidance
9. When symptoms could indicate serious conditions, always recommend medical evaluation

RESPONSE FORMAT:
- Start with traffic light color (🔴, 🟡, or 🟢)
- Explain what the symptoms might indicate
- Give clear action steps
- Specify where to go (facility level)
- Provide home care tips if safe to do so
- End with supportive message"""

        if patient_profile:
            prompt += f"""

PATIENT CONTEXT:
- Stage: {patient_profile.get('stage', 'Unknown')}
- Risk level: {patient_profile.get('risk_level', 'Unknown')}"""

        return prompt

    def _assess_triage(self, query: str, response: str) -> TriageSeverity:
        """Assess the triage level of a query/response (IMCI)"""

        red_keywords = [
            "immediate",
            "emergency",
            "urgent",
            "now",
            "severe",
            "critical",
            "unconscious",
            "heavy bleeding",
            "can't breathe",
            "convulsion",
            "seizure",
            "not feeding",
            "fast breathing",
            "chest indrawing",
        ]

        yellow_keywords = [
            "today",
            "same day",
            "high risk",
            "concerning",
            "fever",
            "pain",
            "bleeding",
            "difficulty",
            "vomiting",
        ]

        query_response = (query + " " + response).lower()

        if any(keyword in query_response for keyword in red_keywords):
            return TriageSeverity.RED
        elif any(keyword in query_response for keyword in yellow_keywords):
            return TriageSeverity.YELLOW
        else:
            return TriageSeverity.GREEN

    def _categorize_query(self, query: str) -> str:
        """Categorize the user query"""
        query_lower = query.lower()

        emergency_keywords = [
            "emergency",
            "urgent",
            "right now",
            "immediately",
            "severe",
            "unconscious",
            "bleeding heavily",
            "can't breathe",
            "convulsion",
            "seizure",
            "dying",
        ]

        symptom_keywords = [
            "pain",
            "bleeding",
            "fever",
            "vomiting",
            "swelling",
            "headache",
            "breathing",
            "cough",
            "diarrhea",
            "rash",
            "itching",
            "burning",
            "discharge",
            "smell",
            "tired",
            "weak",
            "dizzy",
        ]

        if any(keyword in query_lower for keyword in emergency_keywords):
            return "emergency"
        elif any(keyword in query_lower for keyword in symptom_keywords):
            return "symptoms"
        elif "danger" in query_lower or "warning" in query_lower:
            return "danger_signs"
        elif "pregnancy" in query_lower or "pregnant" in query_lower:
            return "pregnancy_info"
        elif "baby" in query_lower or "child" in query_lower:
            return "child_care"
        elif "teen" in query_lower or "adolescent" in query_lower:
            return "adolescent_health"
        else:
            return "general_inquiry"

    def _get_fallback_response(self, query: str) -> str:
        """Provide a fallback response when AI services are unavailable"""
        return f"""Thank you for your question.

Based on your inquiry, we recommend:

🔴 If this is an emergency or severe symptoms:
Go to nearest hospital IMMEDIATELY

🟡 For concerning symptoms:
Visit your health center TODAY

🟢 For general questions:
Contact your healthcare provider at next visit

Remember: When in doubt, seek medical care!

Stay healthy! 💚"""

    @staticmethod
    def _format_list(items: List[str]) -> str:
        """Format a list of items with bullet points"""
        return "\n".join(f"• {item}" for item in items)
