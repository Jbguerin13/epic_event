from models.sql_models import Client, User
from typing import List, Optional
from datetime import date
import re

class ClientController:
    def __init__(self, current_user: User, db):
        self.current_user = current_user
        self.db = db

    def get_all_clients(self) -> List[Client]:
        """Get all clients with permission check"""
        if self.current_user.role.role not in ["manager", "sailor"]:
            raise PermissionError("Not enough permissions to view clients")
        return self.db.query(Client).all()

    def get_client(self, client_id: int) -> Optional[Client]:
        """Get a specific client with permission check"""
        if self.current_user.role.role not in ["manager", "sailor"]:
            raise PermissionError("Not enough permissions to view client")
        return self.db.query(Client).filter(Client.id == client_id).first()

    def create_client(self, name: str, email: str, phone: str, name_company: str, contact_marketing: str) -> Client:
        """Create a new client with validation and permission check"""
        if self.current_user.role.role not in ["manager", "sailor"]:
            raise PermissionError("Not enough permissions to create client")
        if not name or not email or not phone or not name_company or not contact_marketing:
            raise ValueError("every fields are required")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("email format is invalid")
        if not re.match(r"^\+?[0-9]{10,15}$", phone):
            raise ValueError("phone format is invalid")

        client = Client(
            name=name,
            email=email,
            phone=phone,
            name_company=name_company,
            creation_date=date.today(),
            last_update=date.today(),
            contact_marketing=contact_marketing,
            user_id=self.current_user.id
        )

        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    def update_client(self, client_id: int, name: str = None, email: str = None, 
                     phone: str = None, name_company: str = None, 
                     contact_marketing: str = None) -> Optional[Client]:
        """Update a client with validation and permission check"""
        if self.current_user.role.role not in ["manager", "sailor"]:
            raise PermissionError("Not enough permissions to update client")

        client = self.get_client(client_id)
        if not client:
            raise ValueError("client not found")

        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("email format is invalid")

        if phone and not re.match(r"^\+?[0-9]{10,15}$", phone):
            raise ValueError("phone format is invalid")
        if name:
            client.name = name
        if email:
            client.email = email
        if phone:
            client.phone = phone
        if name_company:
            client.name_company = name_company
        if contact_marketing:
            client.contact_marketing = contact_marketing

        client.last_update = date.today()
        self.db.commit()
        self.db.refresh(client)
        return client

    def __del__(self):
        """Close database session when controller is closed"""
        self.db.close() 