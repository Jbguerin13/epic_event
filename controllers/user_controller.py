from models.sql_models import User, UserRoles
from typing import Optional
import re
import sentry_sdk

class UserController:
    def __init__(self, db):
        self.db = db

    def create_user(self, username: str, email: str, password: str, role_name: str) -> Optional[User]:
        """Create a new user with validation"""
        print(f"Tentative de création d'utilisateur: {username}, {email}, {role_name}")
        
        if not username or not email or not password or not role_name:
            raise ValueError("Tous les champs sont obligatoires")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Format d'email invalide")

        if len(password) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères")

        existing_user = self.db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing_user:
            raise ValueError("Le nom d'utilisateur ou l'email existe déjà")

        role = self.db.query(UserRoles).filter(UserRoles.role == role_name).first()
        if not role:
            raise ValueError(f"Rôle invalide: {role_name}")

        print(f"Rôle trouvé: {role.role} (ID: {role.id})")
        
        user = User(
            username=username,
            email=email,
            role_id=role.id
        )
        user.set_password(password)

        print("Ajout de l'utilisateur à la session...")
        self.db.add(user)
        
        print("Tentative de commit...")
        try:
            self.db.commit()
            sentry_sdk.capture_message(f"Utilisateur {username} avec le role {role_name} créé avec succès")
        except Exception as e:
            print(f"Erreur lors du commit: {str(e)}")
            sentry_sdk.capture_message(f"Erreur lors du commit: {str(e)}")
            self.db.rollback()
            raise
        
        self.db.refresh(user)
        print(f"Utilisateur créé avec succès (ID: {user.id})")
        return user 