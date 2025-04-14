from controllers.user_controller import UserController
from models.sql_models import User
import os
from getpass import getpass

class UserView:
    def __init__(self, current_user: User, db):
        self.controller = UserController(db)
        self.db = db
        self.current_user = current_user

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        """Display the user management menu"""
        print("\n=== Gestion des Utilisateurs ===")
        print("1. Créer un nouvel utilisateur")
        print("2. Retour au menu principal")
        return input("\nChoix: ")

    def run_menu(self):
        """Run the user menu loop"""
        if self.current_user.role.role != "manager":
            print("\nAccès refusé. Seul le manager peut gérer les utilisateurs.")
            input("\nAppuyez sur Entrée pour continuer...")
            return

        while True:
            self.clear_screen()
            choice = self.display_menu()
            
            if choice == "1":
                self.create_user()
            elif choice == "2":
                break
            else:
                print("Choix invalide")
            
            input("\nAppuyez sur Entrée pour continuer...")

    def create_user(self):
        """Create a new user"""
        try:
            print("\n=== Création d'un nouvel utilisateur ===")
            username = input("Nom d'utilisateur: ")
            email = input("Email: ")
            password = getpass("Mot de passe: ")
            
            print("\nRôles disponibles:")
            print("1. Manager - Gestion complète du système")
            print("2. Sailor - Gestion des clients et contrats")
            print("3. Support - Gestion des événements")
            
            role_choice = input("\nChoisissez un rôle (1-3): ")
            role_map = {
                "1": "manager",
                "2": "sailor",
                "3": "support"
            }
            
            if role_choice not in role_map:
                raise ValueError("Choix de rôle invalide")
            
            role_name = role_map[role_choice]
            
            user = self.controller.create_user(
                username=username,
                email=email,
                password=password,
                role_name=role_name
            )
            print(f"\nUtilisateur créé avec succès (ID: {user.id})")
        except ValueError as e:
            print(f"\nErreur de validation: {str(e)}")
        except Exception as e:
            print(f"\nUne erreur est survenue: {str(e)}") 