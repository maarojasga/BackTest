from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from . import models, schemas, crud, database, hubspot, clickup, logging_config
from .config import settings
import logging

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

@app.post("/create-contact/")
async def create_contact(contact: schemas.ContactCreate, db: Session = Depends(database.get_db)):
    log_entry = schemas.APILogCreate(endpoint="/create-contact", request_data=contact.json(), result="")
    try:
        result = hubspot.create_contact(contact.dict())
        log_entry.result = str(result)
    except Exception as e:
        log_entry.result = str(e)
    crud.create_log(db, log_entry)
    return result

@app.post("/sync-contacts/")
async def sync_contacts(background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):
    log_entry = schemas.APILogCreate(endpoint="/sync-contacts", request_data="", result="")
    try:
        background_tasks.add_task(sync_contacts_background, db)
        log_entry.result = "Sync initiated"
    except Exception as e:
        log_entry.result = str(e)
    crud.create_log(db, log_entry)
    return {"message": "Sync initiated"}

def sync_contacts_background(db: Session):
    try:
        # Get filtered contacts from HubSpot
        contacts = hubspot.get_filtered_contacts()
        for contact in contacts:
            logging_config.logger.info(f"Processing contact: {contact['id']} - {contact['properties']['email']}")
            # Check if estado_clickup es true
            if contact.get('properties', {}).get('estado_clickup') != 'true':
                logging_config.logger.info(f"Contact {contact['id']} not yet synced with ClickUp. Creating task.")
                # Create the task in ClickUp
                custom_fields = []
                if 'firstname' in contact['properties']:
                    custom_fields.append({"id": "cb06b25c-6f9c-4877-ac7d-ae9e9876c67c", "value": contact['properties']['firstname']})
                if 'lastname' in contact['properties']:
                    custom_fields.append({"id": "ed972c50-732a-4417-8d9a-9a00570bffc0", "value": contact['properties']['lastname']})
                if 'email' in contact['properties']:
                    custom_fields.append({"id": "b6d5af84-6670-4699-81b6-a29a0eddfaee", "value": contact['properties']['email']})
                if 'phone' in contact['properties']:
                    custom_fields.append({"id": "7a53fded-f428-47e4-a4be-b4fa0f882ae4", "value": contact['properties']['phone']})
                if 'website' in contact['properties']:
                    custom_fields.append({"id": "73201812-a98d-4de9-8e52-b998aa3df1fa", "value": contact['properties']['website']})

                task = {
                    "name": contact['properties']['firstname'],
                    "custom_fields": custom_fields
                }
                
                response = clickup.create_task_in_clickup(task, settings.CLICKUP_LIST_ID)
                logging_config.logger.info(f"ClickUp response: {response}")
                if response.get('id'):
                    # Update contact in HubSpot to mark it as synchronized
                    update_response = hubspot.update_contact_property(contact['id'], {'estado_clickup': 'true'})
                    logging_config.logger.info(f"Updated HubSpot contact: {update_response}")
                else:
                    logging_config.logger.error(f"Failed to create ClickUp task for contact {contact['id']}: {response}")
            else:
                logging_config.logger.info(f"Contact {contact['id']} already synced with ClickUp.")
    except Exception as e:
        logging_config.logger.error(f"Error during sync: {str(e)}")
