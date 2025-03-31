from auth import authenticate_user
import os

class AuthView:
    def __init__(self):
        pass

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_login_screen(self):
        """Display the login screen"""
        self.clear_screen()
        print("=== Connexion ===")
        username = input("Nom d'utilisateur: ")
        password = input("Mot de passe: ")
        return username, password

    def display_login_error(self):
        """Display login error message"""
        print("\nErreur: Nom d'utilisateur ou mot de passe incorrect")
        input("\nAppuyez sur Entrée pour réessayer...")

    def login(self):
        """Handle the login process"""
        while True:
            username, password = self.display_login_screen()
            user = authenticate_user(username, password)
            
            if user:
                return user
            else:
                self.display_login_error() 