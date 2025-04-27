from controllers.client_controller import ClientController
from models.sql_models import User
from datetime import date
import os
from permission import Permission

class ClientView:
    def __init__(self, current_user: User, db):
        self.controller = ClientController(current_user, db)
        self.current_user = current_user
        self.db = db

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        """Display the client management menu"""
        print("\n=== Gestion des Clients ===")
        print("1. Liste des clients")
        print("2. Détails d'un client")
        if self.current_user.role.role == "sailor":
            print("3. Créer un client")
            print("4. Modifier un client")
            print("5. Retour au menu principal")
        elif self.current_user.role.role == "admin":
            print("3. Créer un client")
            print("4. Modifier un client")
            print("5. Retour au menu principal")
        else:
            print("3. Retour au menu principal")
        return input("\nChoix: ")

    def run_menu(self):
        """Run the client menu loop"""
        while True:
            self.clear_screen()
            choice = self.display_menu()
            
            if choice == "1":
                self.display_all_clients()
            elif choice == "2":
                try:
                    client_name = input("Nom du client: ")
                    self.display_client(client_name)
                except ValueError:
                    print("Nom invalide")
            elif choice == "3":
                if self.current_user.role.role in ["admin", "sailor"]:
                    self.create_client()
                else:
                    break
            elif choice == "4" and self.current_user.role.role in ["admin", "sailor"]:
                self.update_client()
            elif choice == "5" and self.current_user.role.role in ["admin", "sailor"]:
                break
            elif choice == "3" and self.current_user.role.role not in ["admin", "sailor"]:
                break
            else:
                print("Choix invalide")
            
            input("\nAppuyez sur Entrée pour continuer...")

    def display_all_clients(self):
        """Display all clients"""
        try:
            clients = self.controller.get_all_clients()
            print("\n=== Liste des clients ===")
            for client in clients:
                print(f"\nID: {client.id}")
                print(f"Nom: {client.name}")
                print(f"Entreprise: {client.name_company}")
                print(f"Contact marketing: {client.contact_marketing}")
        except PermissionError as e:
            print(f"\nErreur: {str(e)}")
        except Exception as e:
            print(f"\nUne erreur est survenue: {str(e)}")

    def display_client(self, client_name: str):
        """Display a specific client by name"""
        try:
            client = self.controller.get_client_by_name(client_name)
            if client:
                print(f"\n=== Client {client.name} ===")
                print(f"ID: {client.id}")
                print(f"Nom: {client.name}")
                print(f"Email: {client.email}")
                print(f"Téléphone: {client.phone}")
                print(f"Entreprise: {client.name_company}")
                print(f"Date de création: {client.creation_date}")
                print(f"Dernière mise à jour: {client.last_update}")
                print(f"Contact marketing: {client.contact_marketing}")
            else:
                print(f"\nClient {client_name} non trouvé")
        except PermissionError as e:
            print(f"\nErreur: {str(e)}")
        except Exception as e:
            print(f"\nUne erreur est survenue: {str(e)}")

    def create_client(self):
        """Create a new client"""
        try:
            print("\n=== Création d'un nouveau client ===")
            name = input("Nom du client: ")
            email = input("Email: ")
            phone = input("Téléphone: ")
            name_company = input("Nom de l'entreprise: ")

            client = self.controller.create_client(
                name=name,
                email=email,
                phone=phone,
                name_company=name_company
            )
            print(f"\nClient créé avec succès (ID: {client.id})")
        except ValueError as e:
            print(f"\nErreur de validation: {str(e)}")
        except PermissionError as e:
            print(f"\nErreur: {str(e)}")
        except Exception as e:
            print(f"\nUne erreur est survenue: {str(e)}")

    def update_client(self):
        """Update a client"""
        try:
            print("\n=== Mise à jour d'un client ===")
            client_name = input("Nom du client à modifier: ")
            
            client = self.controller.get_client_by_name(client_name)
            if not client:
                raise ValueError("Client non trouvé")
                
            if self.current_user.role.role == "sailor" and client.contact_marketing != self.current_user.username:
                raise PermissionError("You are not linked to this client, you can't update his details")
            
            print("\nLaissez vide les champs que vous ne souhaitez pas modifier")
            name = input("Nouveau nom (ou vide): ")
            email = input("Nouvel email (ou vide): ")
            phone = input("Nouveau téléphone (ou vide): ")
            name_company = input("Nouveau nom d'entreprise (ou vide): ")

            name = name if name else None
            email = email if email else None
            phone = phone if phone else None
            name_company = name_company if name_company else None

            client = self.controller.update_client(
                client_name=client_name,
                name=name,
                email=email,
                phone=phone,
                name_company=name_company
            )
            print(f"\nClient mis à jour avec succès (ID: {client.id})")
        except ValueError as e:
            print(f"\nErreur de validation: {str(e)}")
        except PermissionError as e:
            print(f"\nErreur: {str(e)}")
        except Exception as e:
            print(f"\nUne erreur est survenue: {str(e)}")

    def __del__(self):
        """Close database session when view is closed"""
        self.db.close() 
            