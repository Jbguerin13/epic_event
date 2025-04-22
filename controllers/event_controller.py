from models.sql_models import Event, User, Contract, Client
from typing import List, Optional
from datetime import date
from permission import Permission

class EventController:
    def __init__(self, current_user: User, db):
        self.current_user = current_user
        self.db = db

    def get_all_events(self) -> List[Event]:
        """Get all events"""
        return self.db.query(Event).all()

    def get_event(self, event_id: int) -> Optional[Event]:
        """Get a specific event by ID"""
        return self.db.query(Event).filter(Event.id == event_id).first()

    def get_event_by_name(self, event_name: str) -> Optional[Event]:
        """Get a specific event by name"""
        return self.db.query(Event).filter(Event.event_name == event_name).first()

    def create_event(self, event_name: str, contract_id: int, event_start_date: date,
                    event_end_date: date, location: str, attendees: int, notes: str = None) -> Event:
        """Create a new event with validation and permission check"""
        if not event_name or not contract_id or not event_start_date or not event_end_date or not location or not attendees:
            raise ValueError("fields are required")
            
        contract = self.db.query(Contract).filter(Contract.id == contract_id).first()
        if not contract:
            raise ValueError("contract not found")

        if self.current_user.role.role == "sailor":
            client = self.db.query(Client).filter(Client.id == contract.client).first()
            if not client:
                raise ValueError("client not found")
            
            if client.contact_marketing != self.current_user.username:
                raise PermissionError("You are not linked to this client")
            
            if not contract.status_contract:
                raise PermissionError("The contract is not signed yet")

        if event_start_date < date.today():
            raise ValueError("start date cannot be in the past")
        if event_end_date < event_start_date:
            raise ValueError("end date must be after start date")
        if attendees <= 0:
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

    def update_event(self, event_id: int, event_name: str = None, contract_id: int = None,
                    event_start_date: date = None, event_end_date: date = None,
                    location: str = None, attendees: int = None, notes: str = None) -> Optional[Event]:
        """Update an event with validation and permission check"""
        event = self.get_event(event_id)
        if not event:
            raise ValueError("Event not found")

        if not Permission.can_update_event(self.current_user, event):
            raise PermissionError("Permission refusée. Vous ne pouvez modifier que les événements qui vous sont assignés.")
            
        if contract_id:
            contract = self.db.query(Contract).filter(Contract.id == contract_id).first()
            if not contract:
                raise ValueError("Contract not found")
            event.contract = contract_id
        if event_start_date:
            if event_start_date < date.today():
                raise ValueError("start date cannot be in the past")
            event.event_start_date = event_start_date
        if event_end_date:
            if event_end_date < event.event_start_date:
                raise ValueError("end date must be after start date")
            event.event_end_date = event_end_date
        if attendees is not None:
            if attendees <= 0:
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

    def __del__(self):
        """Close database session when controller is destroyed"""
        self.db.close() 