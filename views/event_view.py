from controllers.event_controller import EventController
from models.sql_models import User, Contract, Client
from datetime import date, datetime
import os
from permission import Permission

class EventView:
    def __init__(self, current_user: User, db):
        self.controller = EventController(current_user, db)
        self.db = db
        self.current_user = current_user

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        """Display the event management menu"""
        print("\n=== Gestion des Événements ===")
        print("1. Liste des événements")
        print("2. Détails d'un événement")
        if Permission.has_permission(self.current_user, "support"):
            print("3. Créer un événement")
            print("4. Modifier un événement")
            print("5. Retour au menu principal")
        else:
            print("3. Retour au menu principal")
        return input("\nChoix: ")

    def run_menu(self):
        """Run the event menu loop"""
        while True:
            self.clear_screen()
            choice = self.display_menu()
            
            if choice == "1":
                self.display_all_events()
            elif choice == "2":
                try:
                    event_name = input("Nom de l'événement: ")
                    self.display_event(event_name)
                except ValueError:
                    print("Nom invalide")
            elif choice == "3":
                if Permission.has_permission(self.current_user, "support"):
                    self.create_event()
                else:
                    break
            elif choice == "4" and Permission.has_permission(self.current_user, "support"):
                self.update_event()
            elif choice == "5" and Permission.has_permission(self.current_user, "support"):
                break
            elif choice == "3" and not Permission.has_permission(self.current_user, "support"):
                break
            else:
                print("Choix invalide")
            
            input("\nAppuyez sur Entrée pour continuer...")

    def display_all_events(self):
        """Display all events"""
        try:
            events = self.controller.get_all_events()
            print("\n=== Liste des événements ===")
            for event in events:
                contract = self.db.query(Contract).filter(Contract.id == event.contract_id).first()
                client = self.db.query(Client).filter(Client.id == contract.client_id).first()
                print(f"\nNom: {event.event_name}")
                print(f"Client: {client.name} ({client.name_company})")
                print(f"Date de début: {event.event_start_date}")
                print(f"Date de fin: {event.event_end_date}")
                print(f"Lieu: {event.location}")
                print(f"Nombre de participants: {event.attendees}")
                if event.notes:
                    print(f"Notes: {event.notes}")
        except PermissionError as e:
            print(f"\nErreur: {str(e)}")
        except Exception as e:
            print(f"\nUne erreur est survenue: {str(e)}")

    def display_event(self, event_name: str):
        """Display a specific event"""
        try:
            event = self.controller.get_event_by_name(event_name)
            if event:
                contract = self.db.query(Contract).filter(Contract.id == event.contract_id).first()
                client = self.db.query(Client).filter(Client.id == contract.client_id).first()
                print(f"\n=== Événement {event_name} ===")
                print(f"Client: {client.name} ({client.name_company})")
                print(f"Date de début: {event.event_start_date}")
                print(f"Date de fin: {event.event_end_date}")
                print(f"Lieu: {event.location}")
                print(f"Nombre de participants: {event.attendees}")
                if event.notes:
                    print(f"Notes: {event.notes}")
            else:
                print(f"\nÉvénement {event_name} non trouvé")
        except PermissionError as e:
            print(f"\nErreur: {str(e)}")
        except Exception as e:
            print(f"\nUne erreur est survenue: {str(e)}")

    def create_event(self):
        """Create a new event"""
        try:
            print("\n=== Création d'un nouvel événement ===")
            event_name = input("Nom de l'événement: ")
            
            # Afficher la liste des clients
            print("\nListe des clients disponibles :")
            clients = self.db.query(Client).all()
            for client in clients:
                print(f"{client.name} ({client.name_company})")
            
            # Demander le nom du client
            client_name = input("\nNom du client: ")
            client = self.db.query(Client).filter(Client.name == client_name).first()
            if not client:
                raise ValueError("Client non trouvé")
            
            # Vérifier si le client a un contrat
            contract = self.db.query(Contract).filter(Contract.client == client.id).first()
            if not contract:
                raise ValueError("Le client n'a pas de contrat")
            
            start_date = input("Date de début (YYYY-MM-DD): ")
            end_date = input("Date de fin (YYYY-MM-DD): ")
            location = input("Lieu: ")
            attendees = int(input("Nombre de participants: "))
            notes = input("Notes: ")

            event = self.controller.create_event(
                event_name=event_name,
                contract_id=contract.id,
                event_start_date=date.fromisoformat(start_date),
                event_end_date=date.fromisoformat(end_date),
                location=location,
                attendees=attendees,
                notes=notes
            )
            print(f"\nÉvénement créé avec succès pour {client_name}")
        except ValueError as e:
            print(f"\nErreur de validation: {str(e)}")
        except PermissionError as e:
            print(f"\nErreur: {str(e)}")
        except Exception as e:
            print(f"\nUne erreur est survenue: {str(e)}")

    def update_event(self):
        """Update an event"""
        try:
            print("\n=== Mise à jour d'un événement ===")
            event_name = input("Nom de l'événement à modifier: ")
            event = self.controller.get_event_by_name(event_name)
            if not event:
                raise ValueError("Événement non trouvé")
            
            print("\nLaissez vide les champs que vous ne souhaitez pas modifier")
            new_event_name = input("Nouveau nom (ou vide): ")
            
            # Afficher la liste des clients
            print("\nListe des clients disponibles :")
            clients = self.db.query(Client).all()
            for client in clients:
                print(f"{client.name} ({client.name_company})")
            
            # Demander le nom du client
            client_name = input("\nNouveau client (ou vide): ")
            contract_id = None
            if client_name:
                client = self.db.query(Client).filter(Client.name == client_name).first()
                if not client:
                    raise ValueError("Client non trouvé")
                contract = self.db.query(Contract).filter(Contract.client_id == client.id).first()
                if not contract:
                    raise ValueError("Aucun contrat trouvé pour ce client")
                contract_id = contract.id
            
            event_start_date = None
            event_end_date = None
            
            if input("Voulez-vous modifier la date de début ? (o/n): ").lower() == 'o':
                print("\nNouvelle date de début:")
                start_year = int(input("Année: "))
                start_month = int(input("Mois: "))
                start_day = int(input("Jour: "))
                event_start_date = date(start_year, start_month, start_day)
            
            if input("Voulez-vous modifier la date de fin ? (o/n): ").lower() == 'o':
                print("\nNouvelle date de fin:")
                end_year = int(input("Année: "))
                end_month = int(input("Mois: "))
                end_day = int(input("Jour: "))
                event_end_date = date(end_year, end_month, end_day)
            
            location = input("Nouveau lieu (ou vide): ")
            attendees_input = input("Nouveau nombre de participants (ou vide): ")
            notes = input("Nouvelles notes (ou vide): ")

            # Convertir les entrées vides en None
            new_event_name = new_event_name if new_event_name else None
            attendees = int(attendees_input) if attendees_input else None
            notes = notes if notes else None

            event = self.controller.update_event(
                event_id=event.event_id,
                event_name=new_event_name,
                contract_id=contract_id,
                event_start_date=event_start_date,
                event_end_date=event_end_date,
                location=location,
                attendees=attendees,
                notes=notes
            )
            print(f"\nÉvénement mis à jour avec succès")
        except ValueError as e:
            print(f"\nErreur de validation: {str(e)}")
        except PermissionError as e:
            print(f"\nErreur: {str(e)}")
        except Exception as e:
            print(f"\nUne erreur est survenue: {str(e)}") 