from functools import wraps
from models.sql_models import User, Client, Contract, Event

class Permission:
    def __init__(self):
        pass

    @staticmethod
    def has_permission(user: User, required_role: str) -> bool:
        """Check if user has the required role"""
        if user.role.role == "admin":
            return True  # Admin a tous les droits
        elif user.role.role == "manager":
            return required_role in ["manager", "sailor", "support"]
        elif user.role.role == "sailor":
            return required_role in ["sailor", "support"]
        elif user.role.role == "support":
            return required_role == "support"
        return False

    @staticmethod
    def require_role(role: str):
        """Decorator to check if user has required role"""
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if not Permission.has_permission(self.current_user, role):
                    raise PermissionError(f"Permission refusée. Rôle requis: {role}")
                return func(self, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def can_view(user: User) -> bool:
        """Check if user can view data"""
        return True  # Tous les utilisateurs peuvent voir les données

    @staticmethod
    def can_create_client(user: User) -> bool:
        """Check if user can create clients"""
        return user.role.role in ["admin", "sailor"]  # Le manager ne peut pas créer de clients

    @staticmethod
    def can_update_client(user: User, client: object) -> bool:
        """Check if user can update a specific client"""
        if user.role.role == "admin":
            return True
        if user.role.role == "sailor":
            return client.contact_marketing == user.username
        return False

    @staticmethod
    def can_create_contract(user: User) -> bool:
        """Check if user can create contracts"""
        return user.role.role in ["admin", "manager"]

    @staticmethod
    def can_update_contract(user: User, contract: object) -> bool:
        """Check if user can update a specific contract"""
        return user.role.role in ["admin", "manager"]

    @staticmethod
    def can_create_event(user: User, contract: object) -> bool:
        """Check if user can create an event for a specific contract"""
        if user.role.role == "admin":
            return True
        if user.role.role == "sailor":
            client = contract.client
            return client.contact_marketing == user.username and contract.status_contract
        return False

    @staticmethod
    def can_update_event(user: User, event: object) -> bool:
        """Check if user can update a specific event"""
        if user.role.role in ["admin", "manager"]:
            return True
        if user.role.role == "support":
            return event.support_id == user.id
        return False

    @staticmethod
    def can_view_all(user: User) -> bool:
        """Check if user can view all records"""
        return True  # Tous les utilisateurs peuvent voir toutes les données

    @staticmethod
    def can_view_events_without_support(user: User) -> bool:
        """Check if user can view events without support"""
        return user.role.role in ["admin", "manager"]

    @staticmethod
    def can_manage_users(user: User) -> bool:
        """Check if user can manage users (create, update, delete)"""
        return user.role.role in ["admin", "manager"]

    @staticmethod
    def can_assign_support_to_event(user: User) -> bool:
        """Check if user can assign a support to an event"""
        return user.role.role in ["admin", "manager"]

ROLES = {
    "admin": "can do every thing and crud users",
    "manager": "create, update, delete users, create, update contracts, filter the display of the event wich have no support associated, update events",
    "sailor": "sailor can create client and update only their own clients, filter display contracts wich are signed or not, create events only for their clients when contract is signed",
    "support": "support can filter and update events",
}

#classe permission, centraliser la verrif des permissions
#init avec les roles
#methodes pour verifier les permissions des utilisateurs
#faire un décorateur pour les vérifications de permissions à utiliser ensuite dans les controllers


#C'est les permissions et l'auth qui vont être check en premier dans l'examen