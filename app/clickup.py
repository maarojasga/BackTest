import requests
from .config import settings
import logging

CLICKUP_API_URL = "https://api.clickup.com/api/v2"

def create_task_in_clickup(task: dict, list_id: str):
    headers = {
        "Authorization": f"{settings.CLICKUP_API_KEY}",
        "Content-Type": "application/json"
    }
    logging.info(f"Headers: {headers}")
    logging.info(f"Task Payload: {task}")
    
    response = requests.post(f"{CLICKUP_API_URL}/list/{list_id}/task", json=task, headers=headers)
    logging.info(f"Response Status Code: {response.status_code}")
    logging.info(f"Response Headers: {response.headers}")
    logging.info(f"Response from ClickUp: {response.json()}")
    return response.json()
