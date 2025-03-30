import os
from views.client_view import ClientView
from views.contract_view import ContractView
from views.event_view import EventView

class MainMenu:
    def __init__(self, current_user, db):
        self.client_view = ClientView(current_user, db)
        self.contract_view = ContractView(current_user, db)
        self.event_view = EventView(current_user, db)

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        """Display the main menu"""
        print("\n=== Menu Principal ===")
        print("1. Gestion des Clients")
        print("2. Gestion des Contrats")
        print("3. Gestion des Événements")
        print("4. Quitter")
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
            elif choice == "4":
                print("Au revoir!")
                break
            else:
                print("Choix invalide")
                input("\nAppuyez sur Entrée pour continuer...") 