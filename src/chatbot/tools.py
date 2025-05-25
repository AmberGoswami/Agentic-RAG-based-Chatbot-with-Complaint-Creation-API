from langchain.tools import tool
from config import api_service_url
import requests


class Tools:
    url=f"{api_service_url}/complaints"

    @staticmethod 
    @tool
    def create_complaint_tool(name: str, phone_number: str, email: str, complaint_details: str) :
        """Call the external complaint creation API and return the result."""
        
        payload = {
            "name": name,
            "phone_number": phone_number,
            "email": email,
            "complaint_details": complaint_details,
        }

        try:
            response = requests.post(Tools.url, json=payload, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
            return f"Failed to create complaint: {str(e)}"
        
    @staticmethod 
    @tool
    def retrieve_complaint_tool(complaint_id: str) -> dict:
        """Call the external complaint retrieval API and return the result with status."""
        try:
            response = requests.get(f"{Tools.url}/{complaint_id}/", timeout=5)
            if response.status_code == 404:
                return {
                    "status_code": 404,
                    "data": None,
                    "error": "Complaint not found"
                }
            response.raise_for_status()  # Will raise for other 4xx/5xx
            return {
                "status_code": response.status_code,
                "data": response.json()
            }
        except requests.RequestException as e:
            return {
                "status_code": 500,
                "data": None,
                "error": f"Request failed: {str(e)}"
            }