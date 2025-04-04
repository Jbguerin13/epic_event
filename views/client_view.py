from controllers.client_controller import ClientController
from models.sql_models import User
from datetime import date
import os

class ClientView:
    def __init__(self, current_user: User, db):
        self.controller = ClientController(current_user, db)

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        """Display the client management menu"""
        print("\n=== Gestion des Clients ===")
        print("1. Liste des clients")
        print("2. Détails d'un client")
        print("3. Créer un client")
        print("4. Modifier un client")
        print("5. Retour au menu principal")
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
                    client_id = int(input("ID du client: "))
                    self.display_client(client_id)
                except ValueError:
                    print("ID invalide")
            elif choice == "3":
                self.create_client()
            elif choice == "4":
                self.update_client()
            elif choice == "5":
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
                print(f"Email: {client.email}")
                print(f"Téléphone: {client.phone}")
                print(f"Entreprise: {client.name_company}")
                print(f"Date de création: {client.creation_date}")
                print(f"Dernière mise à jour: {client.last_update}")
                print(f"Contact marketing: {client.contact_marketing}")
        except PermissionError as e:
            print(f"\nErreur: {str(e)}")
        except Exception as e:
            print(f"\nUne erreur est survenue: {str(e)}")

    def display_client(self, client_id: int):
        """Display a specific client"""
        try:
            client = self.controller.get_client(client_id)
            if client:
                print(f"\n=== Client {client_id} ===")
                print(f"Nom: {client.name}")
                print(f"Email: {client.email}")
                print(f"Téléphone: {client.phone}")
                print(f"Entreprise: {client.name_company}")
                print(f"Date de création: {client.creation_date}")
                print(f"Dernière mise à jour: {client.last_update}")
                print(f"Contact marketing: {client.contact_marketing}")
            else:
                print(f"\nClient {client_id} non trouvé")
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
            contact_marketing = input("Contact marketing: ")

            client = self.controller.create_client(
                name=name,
                email=email,
                phone=phone,
                name_company=name_company,
                contact_marketing=contact_marketing
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
            client_id = int(input("ID du client à modifier: "))
            
            print("\nLaissez vide les champs que vous ne souhaitez pas modifier")
            name = input("Nouveau nom (ou vide): ")
            email = input("Nouvel email (ou vide): ")
            phone = input("Nouveau téléphone (ou vide): ")
            name_company = input("Nouveau nom d'entreprise (ou vide): ")
            contact_marketing = input("Nouveau contact marketing (ou vide): ")

            # Convertir les entrées vides en None
            name = name if name else None
            email = email if email else None
            phone = phone if phone else None
            name_company = name_company if name_company else None
            contact_marketing = contact_marketing if contact_marketing else None

            client = self.controller.update_client(
                client_id=client_id,
                name=name,
                email=email,
                phone=phone,
                name_company=name_company,
                contact_marketing=contact_marketing
            )
            print(f"\nClient mis à jour avec succès (ID: {client.id})")
        except ValueError as e:
            print(f"\nErreur de validation: {str(e)}")
        except PermissionError as e:
            print(f"\nErreur: {str(e)}")
        except Exception as e:
            print(f"\nUne erreur est survenue: {str(e)}") 
            
            
#dans la vue liste client, afficher seulement l'id et le nom, nom de l'entreprise et le contact marketing
#dans la vue detail client, rentrer le nom plutot que l'id
