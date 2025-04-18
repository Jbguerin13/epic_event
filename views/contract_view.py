from controllers.contract_controller import ContractController
from models.sql_models import User, Client
from datetime import date
import os
from permission import Permission

class ContractView:
    def __init__(self, current_user: User, db):
        self.controller = ContractController(current_user, db)
        self.db = db
        self.current_user = current_user

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        """Display the contract management menu"""
        print("\n=== Gestion des Contrats ===")
        print("1. Liste des contrats")
        print("2. Détails d'un contrat")
        if self.current_user.role.role == "sailor":
            print("3. Modifier un contrat")
            print("4. Retour au menu principal")
        elif self.current_user.role.role in ["admin", "manager"]:
            print("3. Créer un contrat")
            print("4. Modifier un contrat")
            print("5. Retour au menu principal")
        else:
            print("3. Retour au menu principal")
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
                    client_name = input("Nom du client: ")
                    self.display_contract(client_name)
                except ValueError:
                    print("Nom invalide")
            elif choice == "3":
                if self.current_user.role.role == "sailor":
                    self.update_contract()
                elif self.current_user.role.role in ["admin", "manager"]:
                    self.create_contract()
                else:
                    break
            elif choice == "4":
                if self.current_user.role.role == "sailor":
                    break
                elif self.current_user.role.role in ["admin", "manager"]:
                    self.update_contract()
            elif choice == "5" and self.current_user.role.role in ["admin", "manager"]:
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
                client = self.db.query(Client).filter(Client.id == contract.client).first()
                print(f"\nID: {contract.id}")
                print(f"Client: {client.name} ({client.name_company})")
                print(f"Montant total: {contract.total_amount}")
                print(f"Montant restant: {contract.outstanding_amount}")
                print(f"Date de création: {contract.creation_date}")
                print(f"Statut: {'Signé' if contract.status_contract else 'Non signé'}")
        except PermissionError as e:
            print(f"\nErreur: {str(e)}")
        except Exception as e:
            print(f"\nUne erreur est survenue: {str(e)}")

    def display_contract(self, client_name: str):
        """Display a specific contract"""
        try:
            client = self.db.query(Client).filter(Client.name == client_name).first()
            if not client:
                print(f"\nClient {client_name} non trouvé")
                return
                
            contract = self.controller.get_contract_by_client(client.id)
            if contract:
                print(f"\n=== Contrat pour {client_name} ===")
                print(f"ID: {contract.id}")
                print(f"Client: {client.name} ({client.name_company})")
                print(f"Montant total: {contract.total_amount}")
                print(f"Montant restant: {contract.outstanding_amount}")
                print(f"Date de création: {contract.creation_date}")
                print(f"Statut: {'Signé' if contract.status_contract else 'Non signé'}")
            else:
                print(f"\nAucun contrat trouvé pour le client {client_name}")
        except PermissionError as e:
            print(f"\nErreur: {str(e)}")
        except Exception as e:
            print(f"\nUne erreur est survenue: {str(e)}")

    def create_contract(self):
        """Create a new contract"""
        try:
            print("\n=== Création d'un nouveau contrat ===")
            
            print("\nListe des clients disponibles :")
            clients = self.db.query(Client).all()
            for client in clients:
                print(f"{client.name} ({client.name_company})")
            
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
            print(f"\nContrat créé avec succès pour {client_name}")
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
            client_name = input("Nom du client: ")
            client = self.db.query(Client).filter(Client.name == client_name).first()
            if not client:
                raise ValueError("Client non trouvé")
            
            if self.current_user.role.role == "sailor" and client.contact_marketing != self.current_user.username:
                raise PermissionError("You are not linked to this client, you can't update his contract")
            
            contract = self.controller.get_contract_by_client(client.id)
            if not contract:
                raise ValueError("Aucun contrat trouvé pour ce client")
            
            print("\nLaissez vide les champs que vous ne souhaitez pas modifier")
            total_amount_input = input("Nouveau montant total (ou vide): ")
            outstanding_amount_input = input("Nouveau montant restant (ou vide): ")
            status_input = input("Nouveau statut (signé/non signé/vide): ").lower()

            total_amount = int(total_amount_input) if total_amount_input else None
            outstanding_amount = int(outstanding_amount_input) if outstanding_amount_input else None
            status_contract = None
            if status_input:
                status_contract = status_input == "signé"

            contract = self.controller.update_contract(
                contract_id=contract.id,
                total_amount=total_amount,
                outstanding_amount=outstanding_amount,
                status_contract=status_contract
            )
            print(f"\nContrat mis à jour avec succès pour {client_name}")
        except ValueError as e:
            print(f"\nErreur de validation: {str(e)}")
        except PermissionError as e:
            print(f"\nErreur: {str(e)}")
        except Exception as e:
            print(f"\nUne erreur est survenue: {str(e)}") 