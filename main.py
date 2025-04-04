import sentry_sdk
from database import SessionLocal
from models.sql_models import User
from views.main_menu import MainMenu
from views.auth_view import AuthView

sentry_sdk.init(
    dsn="https://bae205cf8dc0f8738ca45ad17008675a@o452613.ingest.us.sentry.io/4509094941425665",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)


def main():
    """Main function"""
    auth_view = AuthView()
    current_user = auth_view.run()
    
    if not current_user:
        print("Échec de l'authentification")
        return

    db = SessionLocal()
    
    try:
        main_menu = MainMenu(current_user, db)
        main_menu.run()
    finally:
        db.close()

if __name__ == "__main__":
    main() 