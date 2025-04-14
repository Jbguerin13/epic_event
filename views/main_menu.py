import os
from views.client_view import ClientView
from views.contract_view import ContractView
from views.event_view import EventView
from views.user_view import UserView
from models.sql_models import User

class MainMenu:
    def __init__(self, current_user: User, db):
        self.current_user = current_user
        self.client_view = ClientView(current_user, db)
        self.contract_view = ContractView(current_user, db)
        self.event_view = EventView(current_user, db)
        self.user_view = UserView(current_user, db)

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        """Display the main menu"""
        print("\n=== Menu Principal ===")
        print(f"Vous êtes connecté avec : {self.current_user.username}")
        print(f"Vous êtes : {self.current_user.role.role}")
        print("\n1. Gestion des Clients")
        print("2. Gestion des Contrats")
        print("3. Gestion des Événements")
        if self.current_user.role.role == "manager":
            print("4. Gestion des Utilisateurs")
        print("5. Quitter")
        return input("\nChoix: ")

    def run(self):
        """Run the main menu loop"""
        while True:
            self.clear_screen()
            choice = self.display_menu()
            
            if choice == "1":
                self.client_view.run_menu()
            elif choice == "2":
                self.contract_view.run_menu()
            elif choice == "3":
                self.event_view.run_menu()
            elif choice == "4" and self.current_user.role.role == "manager":
                self.user_view.run_menu()
            elif choice == "5" or (choice == "4" and self.current_user.role.role != "manager"):
                if choice == "5":
                    print("Au revoir!")
                break
            else:
                print("Choix invalide")
                input("\nAppuyez sur Entrée pour continuer...") 