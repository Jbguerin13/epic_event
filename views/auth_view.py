from auth import authenticate_user
from controllers.user_controller import UserController
from database import SessionLocal
import os
from getpass import getpass

class AuthView:
    def __init__(self):
        self.db = SessionLocal()
        self.user_controller = UserController(self.db)

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_main_menu(self):
        """Display the main authentication menu"""
        self.clear_screen()
        print("=== Epic Events ===")
        print("1. Se connecter")
        print("2. Créer un compte")
        print("3. Quitter")
        return input("\nChoix: ")

    def display_login_screen(self):
        """Display the login screen"""
        self.clear_screen()
        print("=== Connexion ===")
        username = input("Nom d'utilisateur: ")
        password = getpass("Mot de passe: ")
        return username, password

    def display_roles(self):
        """Display available roles"""
        print("\nRôles disponibles :")
        print("1. Manager - Gestion complète du système")
        print("2. Sailor - Gestion des clients et contrats")
        print("3. Support - Gestion des événements")
        choice = input("\nChoisissez un rôle (1-3): ")
        
        role_map = {
            "1": "manager",
            "2": "sailor",
            "3": "support"
        }
        
        if choice not in role_map:
            raise ValueError("Choix de rôle invalide")
            
        return role_map[choice]

    def display_register_screen(self):
        """Display the registration screen"""
        self.clear_screen()
        print("=== Création de compte ===")
        username = input("Nom d'utilisateur: ")
        email = input("Email: ")
        password = getpass("Mot de passe: ")
        confirm_password = getpass("Confirmer le mot de passe: ")
        
        if password != confirm_password:
            raise ValueError("Les mots de passe ne correspondent pas")
            
        role = self.display_roles()
        return username, email, password, role

    def display_login_error(self):
        """Display login error message"""
        print("\nErreur: Nom d'utilisateur ou mot de passe incorrect")
        input("\nAppuyez sur Entrée pour réessayer...")

    def display_register_error(self, error_message: str):
        """Display registration error message"""
        print(f"\nErreur: {error_message}")
        input("\nAppuyez sur Entrée pour réessayer...")

    def display_register_success(self):
        """Display registration success message"""
        print("\nCompte créé avec succès !")
        input("\nAppuyez sur Entrée pour continuer...")

    def login(self):
        """Handle the login process"""
        while True:
            username, password = self.display_login_screen()
            user = authenticate_user(username, password)
            
            if user:
                return user
            else:
                self.display_login_error()

    def register(self):
        """Handle the registration process"""
        while True:
            try:
                username, email, password, role = self.display_register_screen()
                user = self.user_controller.create_user(
                    username=username,
                    email=email,
                    password=password,
                    role_name=role
                )
                self.display_register_success()
                return user
            except ValueError as e:
                self.display_register_error(str(e))

    def run(self):
        """Run the authentication process"""
        while True:
            choice = self.display_main_menu()
            
            if choice == "1":
                return self.login()
            elif choice == "2":
                return self.register()
            elif choice == "3":
                print("Au revoir !")
                exit()
            else:
                print("Choix invalide")
                input("\nAppuyez sur Entrée pour continuer...")
#return le current user et casser la boucle while

    def __del__(self):
        """Close database session when view is closed"""
        self.db.close()