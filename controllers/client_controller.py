from models.sql_models import Client, User
from typing import List, Optional
from datetime import date
import re
from permission import Permission
from sqlalchemy.orm import joinedload

class ClientController:
    def __init__(self, current_user: User, db):
        self.db = db
        self.current_user = db.query(User).options(joinedload(User.role)).filter(User.id == current_user.id).first()

    def get_all_clients(self) -> List[Client]:
        """Get all clients"""
        return self.db.query(Client).all()

    def get_client(self, client_id: int) -> Optional[Client]:
        """Get a specific client by ID"""
        return self.db.query(Client).filter(Client.id == client_id).first()

    def get_client_by_name(self, name: str) -> Optional[Client]:
        """Get a specific client by name"""
        return self.db.query(Client).filter(Client.name == name).first()

    def create_client(self, name: str, email: str, phone: str, name_company: str) -> Client:
        """Create a new client with validation and permission check"""
        if not Permission.can_create_client(self.current_user):
            raise PermissionError("Permission refusée. Rôle requis: sailor")
            
        if not name or not email or not phone or not name_company:
            raise ValueError("Tous les champs sont obligatoires")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Format d'email invalide")
        if not re.match(r"^\+?[0-9]{10,15}$", phone):
            raise ValueError("Format de numéro de téléphone invalide")

        contact_marketing = self.current_user.username

        client = Client(
            name=name,
            email=email,
            phone=phone,
            name_company=name_company,
            creation_date=date.today(),
            last_update=date.today(),
            contact_marketing=contact_marketing
        )

        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    def update_client(self, client_name: str, name: str = None, email: str = None, 
                     phone: str = None, name_company: str = None) -> Optional[Client]:
        """Update a client with validation and permission check"""
        client = self.get_client_by_name(client_name)
        if not client:
            raise ValueError("Client non trouvé")

        if self.current_user.role.role == "sailor":
            if client.contact_marketing != self.current_user.username:
                raise PermissionError("You are not linked to this client, you can't update his details")
            
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Format d'email invalide")

        if phone and not re.match(r"^\+?[0-9]{10,15}$", phone):
            raise ValueError("Format de numéro de téléphone invalide")

        if name:
            client.name = name
        if email:
            client.email = email
        if phone:
            client.phone = phone
        if name_company:
            client.name_company = name_company

        client.last_update = date.today()
        self.db.commit()
        self.db.refresh(client)
        return client

    def __del__(self):
        """Close database session when controller is closed"""
        self.db.close() 