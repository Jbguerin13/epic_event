from database import SessionLocal
from models.sql_models import UserRoles

def init_roles():
    """Initialize roles in the database"""
    db = SessionLocal()
    try:
        # Vérifier si les rôles existent déjà
        existing_roles = db.query(UserRoles).all()
        if existing_roles:
            print("Les rôles existent déjà dans la base de données.")
            return

        # Créer les rôles
        roles = [
            UserRoles(role="manager"),
            UserRoles(role="sailor"),
            UserRoles(role="support")
        ]

        # Insérer les rôles dans la base de données
        for role in roles:
            db.add(role)
        
        db.commit()
        print("Rôles créés avec succès !")
        
    except Exception as e:
        print(f"Erreur lors de la création des rôles : {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_roles() 