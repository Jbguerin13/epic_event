from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    phone = Column(String(250), nullable=False)
    name_company = Column(String(250), nullable=False)
    creation_date = Column(Date, nullable=False)
    last_update = Column(Date, nullable=False)
    contact_marketing = Column(String(250), nullable=False)
    
    
class Contract(Base):
    __tablename__ = "contracts"
    
    id = Column(Integer, primary_key=True)
    client = Column(String(250), ForeignKey("clients.id"), nullable=False)
    total_amount = Column(Integer, nullable=False)
    outstanding_amount = Column(Integer, nullable=False)
    creation_date = Column(Date, nullable=False)
    status_contract = Column(Boolean, nullable=False)


class Event(Base):
    __tablename__ = "events"
    
    event_id = Column(Integer, primary_key=True)
    event_name = Column(String(250), nullable=False)
    contract = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    event_start_date = Column(Date, nullable=False)
    event_end_date = Column(Date, nullable=False)
    location = Column(String(250), nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(String(500), nullable=True)

#manque classe User et classe Role
#manque classe UserRoles
