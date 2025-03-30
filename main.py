from database import SessionLocal
from models.sql_models import User
from views.main_menu import MainMenu
from auth import authenticate_user

def main():
    """Main function"""
    print("=== Connexion ===")
    username = input("Nom d'utilisateur: ")
    password = input("Mot de passe: ")
    
    current_user = authenticate_user(username, password)
    if not current_user:
        print("Authentification échouée")
        return

    db = SessionLocal()
    
    try:
        main_menu = MainMenu(current_user, db)
        main_menu.run()
    finally:
        db.close()

if __name__ == "__main__":
    main() 