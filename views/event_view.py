from controllers.event_controller import EventController
from models.sql_models import User
from datetime import date, datetime
import os

class EventView:
    def __init__(self, current_user: User, db):
        self.controller = EventController(current_user, db)

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        """Display the event management menu"""
        print("\n=== Gestion des Événements ===")
        print("1. Liste des événements")
        print("2. Détails d'un événement")
        print("3. Créer un événement")
        print("4. Modifier un événement")
        print("5. Retour au menu principal")
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
                    event_id = int(input("ID de l'événement: "))
                    self.display_event(event_id)
                except ValueError:
                    print("ID invalide")
            elif choice == "3":
                self.create_event()
            elif choice == "4":
                self.update_event()
            elif choice == "5":
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
                print(f"\nID: {event.event_id}")
                print(f"Nom: {event.event_name}")
                print(f"Contrat ID: {event.contract_id}")
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

    def display_event(self, event_id: int):
        """Display a specific event"""
        try:
            event = self.controller.get_event(event_id)
            if event:
                print(f"\n=== Événement {event_id} ===")
                print(f"Nom: {event.event_name}")
                print(f"Contrat ID: {event.contract_id}")
                print(f"Date de début: {event.event_start_date}")
                print(f"Date de fin: {event.event_end_date}")
                print(f"Lieu: {event.location}")
                print(f"Nombre de participants: {event.attendees}")
                if event.notes:
                    print(f"Notes: {event.notes}")
            else:
                print(f"\nÉvénement {event_id} non trouvé")
        except PermissionError as e:
            print(f"\nErreur: {str(e)}")
        except Exception as e:
            print(f"\nUne erreur est survenue: {str(e)}")

    def create_event(self):
        """Create a new event"""
        try:
            print("\n=== Création d'un nouvel événement ===")
            event_name = input("Nom de l'événement: ")
            contract_id = int(input("ID du contrat: "))
            
            print("\nDate de début:")
            start_year = int(input("Année: "))
            start_month = int(input("Mois: "))
            start_day = int(input("Jour: "))
            event_start_date = date(start_year, start_month, start_day)
            
            print("\nDate de fin:")
            end_year = int(input("Année: "))
            end_month = int(input("Mois: "))
            end_day = int(input("Jour: "))
            event_end_date = date(end_year, end_month, end_day)
            
            location = input("Lieu: ")
            attendees = int(input("Nombre de participants: "))
            notes = input("Notes (optionnel): ")

            event = self.controller.create_event(
                event_name=event_name,
                contract_id=contract_id,
                event_start_date=event_start_date,
                event_end_date=event_end_date,
                location=location,
                attendees=attendees,
                notes=notes if notes else None
            )
            print(f"\nÉvénement créé avec succès (ID: {event.event_id})")
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
            event_id = int(input("ID de l'événement à modifier: "))
            
            print("\nLaissez vide les champs que vous ne souhaitez pas modifier")
            event_name = input("Nouveau nom (ou vide): ")
            contract_id_input = input("Nouvel ID contrat (ou vide): ")
            
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
            event_name = event_name if event_name else None
            contract_id = int(contract_id_input) if contract_id_input else None
            attendees = int(attendees_input) if attendees_input else None
            notes = notes if notes else None

            event = self.controller.update_event(
                event_id=event_id,
                event_name=event_name,
                contract_id=contract_id,
                event_start_date=event_start_date,
                event_end_date=event_end_date,
                location=location,
                attendees=attendees,
                notes=notes
            )
            print(f"\nÉvénement mis à jour avec succès (ID: {event.event_id})")
        except ValueError as e:
            print(f"\nErreur de validation: {str(e)}")
        except PermissionError as e:
            print(f"\nErreur: {str(e)}")
        except Exception as e:
            print(f"\nUne erreur est survenue: {str(e)}") 