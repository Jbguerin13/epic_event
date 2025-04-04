from functools import wraps
from models.sql_models import User

class Permission:
    def __init__(self):
        pass

    @staticmethod
    def has_permission(user: User, required_role: str) -> bool:
        """Check if user has the required role"""
        if user.role.role == "manager":
            return True  # Manager a tous les droits
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
    def can_create_client(user: User) -> bool:
        """Check if user can create clients"""
        return Permission.has_permission(user, "sailor")

    @staticmethod
    def can_update_client(user: User) -> bool:
        """Check if user can update clients"""
        return Permission.has_permission(user, "sailor")

    @staticmethod
    def can_create_contract(user: User) -> bool:
        """Check if user can create contracts"""
        return Permission.has_permission(user, "sailor")

    @staticmethod
    def can_update_contract(user: User) -> bool:
        """Check if user can update contracts"""
        return Permission.has_permission(user, "sailor")

    @staticmethod
    def can_create_event(user: User) -> bool:
        """Check if user can create events"""
        return Permission.has_permission(user, "sailor")

    @staticmethod
    def can_update_event(user: User) -> bool:
        """Check if user can update events"""
        return Permission.has_permission(user, "support")

    @staticmethod
    def can_view_all(user: User) -> bool:
        """Check if user can view all records"""
        return Permission.has_permission(user, "manager")

ROLES = {
    "manager": " manager can create, update, delete collaborators, manage contracts, and filter events",
    "sailor": "sailor can create and update clients, update contracts, create events",
    "support": "support can filter and update events",
}

#classe permission, centraliser la verrif des permissions
#init avec les roles
#methodes pour verifier les permissions des utilisateurs
#faire un décorateur pour les vérifications de permissions à utiliser ensuite dans les controllers


#C'est les permissions et l'auth qui vont être check en premier dans l'examen