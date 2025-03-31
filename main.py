from database import SessionLocal
from models.sql_models import User
from views.main_menu import MainMenu
from views.auth_view import AuthView

def main():
    """Main function"""
    # Authentification
    auth_view = AuthView()
    current_user = auth_view.login()
    
    if not current_user:
        print("Échec de l'authentification")
        return

    db = SessionLocal()
    #notion de transaction != de connexion
    try:
        main_menu = MainMenu(current_user, db)
        main_menu.run()
    finally:
        db.close()

if __name__ == "__main__":
    main() 