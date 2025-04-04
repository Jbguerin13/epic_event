from controllers.contract_controller import ContractController
from models.sql_models import User, Client
from datetime import date
import os

class ContractView:
    def __init__(self, current_user: User, db):
        self.controller = ContractController(current_user, db)
        self.db = db

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        """Display the contract management menu"""
        print("\n=== Gestion des Contrats ===")
        print("1. Liste des contrats")
        print("2. Détails d'un contrat")
        print("3. Créer un contrat")
        print("4. Modifier un contrat")
        print("5. Retour au menu principal")
        return input("\nChoix: ")

    def run_menu(self):
        """Run the contract menu loop"""
        while True:
            self.clear_screen()
            choice = self.display_menu()
            
            if choice == "1":
                self.display_all_contracts()
            elif choice == "2":
                try:
                    contract_id = int(input("ID du contrat: "))
                    self.display_contract(contract_id)
                except ValueError:
                    print("ID invalide")
            elif choice == "3":
                self.create_contract()
            elif choice == "4":
                self.update_contract()
            elif choice == "5":
                break
            else:
                print("Choix invalide")
            
            input("\nAppuyez sur Entrée pour continuer...")

    def display_all_contracts(self):
        """Display all contracts"""
        try:
            contracts = self.controller.get_all_contracts()
            print("\n=== Liste des contrats ===")
            for contract in contracts:
                print(f"\nID: {contract.id}")
                print(f"Client ID: {contract.client_id}")
                print(f"Montant total: {contract.total_amount}")
                print(f"Montant restant: {contract.outstanding_amount}")
                print(f"Date de création: {contract.creation_date}")
                print(f"Statut: {'Signé' if contract.status_contract else 'Non signé'}")
        except PermissionError as e:
            print(f"\nErreur: {str(e)}")
        except Exception as e:
            print(f"\nUne erreur est survenue: {str(e)}")

    def display_contract(self, contract_id: int):
        """Display a specific contract"""
        try:
            contract = self.controller.get_contract(contract_id)
            if contract:
                print(f"\n=== Contrat {contract_id} ===")
                print(f"Client ID: {contract.client_id}")
                print(f"Montant total: {contract.total_amount}")
                print(f"Montant restant: {contract.outstanding_amount}")
                print(f"Date de création: {contract.creation_date}")
                print(f"Statut: {'Signé' if contract.status_contract else 'Non signé'}")
            else:
                print(f"\nContrat {contract_id} non trouvé")
        except PermissionError as e:
            print(f"\nErreur: {str(e)}")
        except Exception as e:
            print(f"\nUne erreur est survenue: {str(e)}")

    def create_contract(self):
        """Create a new contract"""
        try:
            print("\n=== Création d'un nouveau contrat ===")
            
            # Afficher la liste des clients
            print("\nListe des clients disponibles :")
            clients = self.db.query(Client).all()
            for client in clients:
                print(f"ID: {client.id} - {client.name} ({client.name_company})")
            
            # Demander le nom du client
            client_name = input("\nNom du client: ")
            client = self.db.query(Client).filter(Client.name == client_name).first()
            if not client:
                raise ValueError("Client non trouvé")
            
            total_amount = int(input("Montant total: "))
            outstanding_amount = int(input("Montant restant à payer: "))
            status_contract = input("Contrat signé ? (oui/non): ").lower() == "oui"

            contract = self.controller.create_contract(
                client_id=client.id,
                total_amount=total_amount,
                outstanding_amount=outstanding_amount,
                status_contract=status_contract
            )
            print(f"\nContrat créé avec succès (ID: {contract.id})")
        except ValueError as e:
            print(f"\nErreur de validation: {str(e)}")
        except PermissionError as e:
            print(f"\nErreur: {str(e)}")
        except Exception as e:
            print(f"\nUne erreur est survenue: {str(e)}")

    def update_contract(self):
        """Update a contract"""
        try:
            print("\n=== Mise à jour d'un contrat ===")
            contract_id = int(input("ID du contrat à modifier: "))
            
            print("\nLaissez vide les champs que vous ne souhaitez pas modifier")
            client_id_input = input("Nouvel ID client (ou vide): ")
            total_amount_input = input("Nouveau montant total (ou vide): ")
            outstanding_amount_input = input("Nouveau montant restant (ou vide): ")
            status_input = input("Nouveau statut (signé/non signé/vide): ").lower()

            # Convertir les entrées vides en None
            client_id = int(client_id_input) if client_id_input else None
            total_amount = int(total_amount_input) if total_amount_input else None
            outstanding_amount = int(outstanding_amount_input) if outstanding_amount_input else None
            status_contract = None
            if status_input:
                status_contract = status_input == "signé"

            contract = self.controller.update_contract(
                contract_id=contract_id,
                client_id=client_id,
                total_amount=total_amount,
                outstanding_amount=outstanding_amount,
                status_contract=status_contract
            )
            print(f"\nContrat mis à jour avec succès (ID: {contract.id})")
        except ValueError as e:
            print(f"\nErreur de validation: {str(e)}")
        except PermissionError as e:
            print(f"\nErreur: {str(e)}")
        except Exception as e:
            print(f"\nUne erreur est survenue: {str(e)}") 