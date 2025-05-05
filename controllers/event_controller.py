from models.sql_models import Event, User, Contract, Client
from typing import List, Optional
from datetime import date
from permission import Permission
import sentry_sdk

class EventController:
    def __init__(self, current_user: User, db):
        self.current_user = current_user
        self.db = db

    def get_all_events(self) -> List[Event]:
        """Get all events"""
        return self.db.query(Event).all()

    def get_event(self, event_id: int) -> Optional[Event]:
        """Get a specific event by ID"""
        return self.db.query(Event).filter(Event.event_id == event_id).first()

    def get_event_by_name(self, event_name: str) -> Optional[Event]:
        """Get a specific event by name"""
        return self.db.query(Event).filter(Event.event_name == event_name).first()

    def create_event(self, event_name: str, contract_id: int, event_start_date: date,
                    event_end_date: date, location: str, attendees: int, notes: str = None) -> Event:
        """Create a new event with validation and permission check"""
        try:
            if not event_name or not contract_id or not event_start_date or not event_end_date or not location or not attendees:
                sentry_sdk.capture_message(f"Tentative de création d'événement avec des champs manquants par {self.current_user.username}")
                raise ValueError("fields are required")
                
            contract = self.db.query(Contract).filter(Contract.id == contract_id).first()
            if not contract:
                sentry_sdk.capture_message(f"Contrat non trouvé pour la création d'événement: {contract_id} par {self.current_user.username}")
                raise ValueError("contract not found")

            if self.current_user.role.role == "sailor":
                client = self.db.query(Client).filter(Client.id == contract.client).first()
                if not client:
                    sentry_sdk.capture_message(f"Client non trouvé pour la création d'événement par {self.current_user.username}")
                    raise ValueError("client not found")
                
                if client.contact_marketing != self.current_user.username:
                    sentry_sdk.capture_message(f"Tentative de création d'événement pour un client non assigné par {self.current_user.username}")
                    raise PermissionError("You are not linked to this client")
                
                if not contract.status_contract:
                    sentry_sdk.capture_message(f"Tentative de création d'événement pour un contrat non signé par {self.current_user.username}")
                    raise PermissionError("The contract is not signed yet")

            if event_start_date < date.today():
                sentry_sdk.capture_message(f"Date de début invalide: {event_start_date} par {self.current_user.username}")
                raise ValueError("start date cannot be in the past")
            if event_end_date < event_start_date:
                sentry_sdk.capture_message(f"Date de fin invalide: {event_end_date} par {self.current_user.username}")
                raise ValueError("end date must be after start date")
            if attendees <= 0:
                sentry_sdk.capture_message(f"Nombre d'invités invalide: {attendees} par {self.current_user.username}")
                raise ValueError("attendees must be greater than 0")

            event = Event(
                event_name=event_name,
                contract=contract_id,
                event_start_date=event_start_date,
                event_end_date=event_end_date,
                location=location,
                attendees=attendees,
                notes=notes
            )

            self.db.add(event)
            self.db.commit()
            self.db.refresh(event)
            return event
        except (ValueError, PermissionError) as e:
            sentry_sdk.capture_exception(e)
            raise

    def update_event(self, event_id: int, event_name: str = None, contract_id: int = None,
                    event_start_date: date = None, event_end_date: date = None,
                    location: str = None, attendees: int = None, notes: str = None) -> Optional[Event]:
        """Update an event with validation and permission check"""
        try:
            event = self.get_event(event_id)
            if not event:
                sentry_sdk.capture_message(f"Événement non trouvé: {event_id} par {self.current_user.username}")
                raise ValueError("Event not found")

            if not Permission.can_update_event(self.current_user, event):
                sentry_sdk.capture_message(f"Tentative de modification d'événement sans permission par {self.current_user.username}")
                raise PermissionError("Permission refusée. Vous ne pouvez modifier que les événements qui vous sont assignés.")
                
            if contract_id:
                contract = self.db.query(Contract).filter(Contract.id == contract_id).first()
                if not contract:
                    sentry_sdk.capture_message(f"Contrat non trouvé pour la modification d'événement: {contract_id} par {self.current_user.username}")
                    raise ValueError("Contract not found")
                event.contract = contract_id
            if event_start_date:
                if event_start_date < date.today():
                    sentry_sdk.capture_message(f"Date de début invalide: {event_start_date} par {self.current_user.username}")
                    raise ValueError("start date cannot be in the past")
                event.event_start_date = event_start_date
            if event_end_date:
                if event_end_date < event.event_start_date:
                    sentry_sdk.capture_message(f"Date de fin invalide: {event_end_date} par {self.current_user.username}")
                    raise ValueError("end date must be after start date")
                event.event_end_date = event_end_date
            if attendees is not None:
                if attendees <= 0:
                    sentry_sdk.capture_message(f"Nombre d'invités invalide: {attendees} par {self.current_user.username}")
                    raise ValueError("attendees must be greater than 0")
                event.attendees = attendees

            if event_name:
                event.event_name = event_name
            if location:
                event.location = location
            if notes is not None:
                event.notes = notes

            self.db.commit()
            self.db.refresh(event)
            return event
        except (ValueError, PermissionError) as e:
            sentry_sdk.capture_exception(e)
            raise

    def __del__(self):
        """Close database session when controller is destroyed"""
        self.db.close()

    def get_user_by_name(self, username: str) -> Optional[User]:
        """Get a user by username"""
        return self.db.query(User).filter(User.username == username).first()

    def assign_support_to_event(self, event_name: str, support_name: str) -> Optional[Event]:
        """Assign a support to an event"""
        try:
            event = self.get_event_by_name(event_name)
            if not event:
                sentry_sdk.capture_message(f"Événement non trouvé pour l'assignation: {event_name} par {self.current_user.username}")
                raise ValueError("Event not found")

            support = self.get_user_by_name(support_name)
            if not support:
                sentry_sdk.capture_message(f"Support non trouvé: {support_name} par {self.current_user.username}")
                raise ValueError("Support user not found")
            
            if support.role.role != "support":
                sentry_sdk.capture_message(f"Tentative d'assignation à un utilisateur non support: {support_name} par {self.current_user.username}")
                raise ValueError("User must be a support")

            event.support_id = support.id
            self.db.commit()
            self.db.refresh(event)
            return event
        except (ValueError, PermissionError) as e:
            sentry_sdk.capture_exception(e)
            raise 