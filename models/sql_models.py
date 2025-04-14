from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

Base = declarative_base()

class UserRoles(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True)
    role = Column(String(250), nullable=False, unique=True)
    users = relationship("User", back_populates="role")

    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    email = Column(String(250), nullable=False, unique=True)
    password_hash = Column(String(512), nullable=False)
    role_id = Column(Integer, ForeignKey("user_roles.id"), nullable=False)
    role = relationship("UserRoles", back_populates="users")

    def set_password(self, password):
        self.password_hash = PasswordHasher().hash(password)
    
    def verify_password(self, password):
        try:
            return PasswordHasher().verify(self.password_hash, password)
        except VerifyMismatchError:
            return False
    


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
