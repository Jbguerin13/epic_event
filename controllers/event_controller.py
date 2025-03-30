from models.sql_models import Event, User, Contract
from typing import List, Optional
from datetime import date

class EventController:
    def __init__(self, current_user: User, db):
        self.current_user = current_user
        self.db = db

    def get_all_events(self) -> List[Event]:
        """Get all events with permission check"""
        if self.current_user.role.role not in ["manager", "sailor", "support"]:
            raise PermissionError("Not enough permissions to view events")
        return self.db.query(Event).all()

    def get_event(self, event_id: int) -> Optional[Event]:
        """Get a specific event with permission check"""
        if self.current_user.role.role not in ["manager", "sailor", "support"]:
            raise PermissionError("Not enough permissions to view event")
        return self.db.query(Event).filter(Event.event_id == event_id).first()

    def create_event(self, event_name: str, contract_id: int, event_start_date: date,
                    event_end_date: date, location: str, attendees: int, notes: str = None) -> Event:
        """Create a new event with validation and permission check"""
        if self.current_user.role.role not in ["manager", "sailor", "support"]:
            raise PermissionError("Not enough permissions to create event")
        if not event_name or not contract_id or not event_start_date or not event_end_date or not location or not attendees:
            raise ValueError("fields are required")
        contract = self.db.query(Contract).filter(Contract.id == contract_id).first()
        if not contract:
            raise ValueError("contract not found")
        if event_start_date < date.today():
            raise ValueError("start date cannot be in the past")
        if event_end_date < event_start_date:
            raise ValueError("end date must be after start date")
        if attendees <= 0:
            raise ValueError("attendees must be greater than 0")

        event = Event(
            event_name=event_name,
            contract_id=contract_id,
            event_start_date=event_start_date,
            event_end_date=event_end_date,
            location=location,
            attendees=attendees,
            notes=notes,
            user_id=self.current_user.id
        )

        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def update_event(self, event_id: int, event_name: str = None, contract_id: int = None,
                    event_start_date: date = None, event_end_date: date = None,
                    location: str = None, attendees: int = None, notes: str = None) -> Optional[Event]:
        """Update an event with validation and permission check"""
        if self.current_user.role.role not in ["manager", "sailor", "support"]:
            raise PermissionError("Not enough permissions to update event")
        event = self.get_event(event_id)
        if not event:
            raise ValueError("Event not found")
        if contract_id:
            contract = self.db.query(Contract).filter(Contract.id == contract_id).first()
            if not contract:
                raise ValueError("Contract not found")
            event.contract_id = contract_id
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