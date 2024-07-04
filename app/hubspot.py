import requests
from .config import settings

HUBSPOT_API_URL = "https://api.hubapi.com"

def create_contact(contact: dict):
    """ Create Hubspot contact """
    headers = {"Authorization": f"Bearer {settings.HUBSPOT_API_KEY}", "Content-Type": "application/json"}
    response = requests.post(HUBSPOT_API_URL + '/crm/v3/objects/contacts', json={"properties": contact}, headers=headers)
    return response.json()

def get_filtered_contacts():
    """ Gets Hubspot contacts where the custom field estado_clickup is set to true. """
    headers = {"Authorization": f"Bearer {settings.HUBSPOT_API_KEY}", "Content-Type": "application/json"}
    url = f"{HUBSPOT_API_URL}/crm/v3/objects/contacts/search"
    
    query = {
        "filterGroups": [
            {
                "filters": [
                    {
                        "propertyName": "estado_clickup",
                        "operator": "NEQ",
                        "value": "true"
                    }
                ]
            }
        ],
        "properties": ["firstname", "lastname", "email", "phone", "website", "estado_clickup"],
        "limit": 100
    }
    
    response = requests.post(url, json=query, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch contacts: {response.status_code}, {response.text}")
        return []
    
    contacts = response.json().get("results", [])
    return contacts

def update_contact_property(contact_id: str, properties: dict):
    """ Update a Hubspot contact property, in this case we will use it to update the property estado_clickup. """
    headers = {"Authorization": f"Bearer {settings.HUBSPOT_API_KEY}", "Content-Type": "application/json"}
    update_url = f"{HUBSPOT_API_URL}/crm/v3/objects/contacts/{contact_id}"
    data = {"properties": properties}
    response = requests.patch(update_url, json=data, headers=headers)
    return response.json()
