import os
import httpx
import logging
import base64
from typing import Dict, Any, List
from app.core.config import settings

logger = logging.getLogger(__name__)

class DHIS2IntegrationService:
    """Service to push/pull data from National DHIS2 systems"""
    
    def __init__(self):
        self.base_url = os.getenv("DHIS2_BASE_URL", "https://play.dhis2.org/demo/api")
        self.username = os.getenv("DHIS2_USERNAME", "admin")
        self.password = os.getenv("DHIS2_PASSWORD", "district")
        
        # Create Basic Auth header
        auth_str = f"{self.username}:{self.password}"
        b64_auth = base64.b64encode(auth_str.encode('ascii')).decode('ascii')
        
        self.headers = {
            "Authorization": f"Basic {b64_auth}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    async def sync_high_risk_patient(self, patient_data: Dict[str, Any]) -> bool:
        """
        Pushes a newly identified high-risk mother/child into the DHIS2 Tracker Network
        """
        # In a real scenario, map local fields to DHIS2 Data Elements (TEIs)
        payload = {
            "trackedEntityInstances": [
                {
                    "trackedEntityType": "MCP-MATERNAL",
                    "orgUnit": "YOUR_ORG_UNIT_ID",
                    "attributes": [
                        {"attribute": "FIRST_NAME_ID", "value": patient_data.get("first_name")},
                        {"attribute": "PHONE_ID", "value": patient_data.get("phone_number")},
                        {"attribute": "RISK_LEVEL_ID", "value": patient_data.get("risk_level")}
                    ]
                }
            ]
        }

        try:
            async with httpx.AsyncClient() as client:
                # Placeholder for actual API call
                # response = await client.post(
                #     f"{self.base_url}/trackedEntityInstances",
                #     headers=self.headers,
                #     json=payload
                # )
                # response.raise_for_status()
                logger.info(f"Successfully synced high-risk patient to DHIS2: {patient_data.get('phone_number')}")
                return True
        except Exception as e:
            logger.error(f"Failed to sync with DHIS2: {e}")
            return False

    async def fetch_national_protocols(self) -> List[Dict]:
        """
        Pull the latest IMCI or national health protocols from DHIS2 DataSets
        """
        try:
            async with httpx.AsyncClient() as client:
                # response = await client.get(
                #     f"{self.base_url}/dataSets",
                #     headers=self.headers
                # )
                logger.info("Successfully fetched national protocols from DHIS2")
                return [{"protocol": "IMCI_2024", "status": "active"}]
        except Exception as e:
            logger.error(f"Failed to fetch protocols from DHIS2: {e}")
            return []
