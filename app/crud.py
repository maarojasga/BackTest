from sqlalchemy.orm import Session
from . import models, schemas

def create_log(db: Session, log: schemas.APILogCreate):
    db_log = models.APILog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log
