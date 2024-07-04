from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime

class APILog(Base):
    __tablename__ = "api_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    endpoint = Column(String, index=True)
    request_data = Column(String)
    result = Column(String)
