from database import engine
from sqlalchemy import text

def add_user_id_to_clients():
    """Add user_id column to clients table"""
    with engine.connect() as connection:
        # Vérifier si la colonne existe déjà
        result = connection.execute(text("""
            SELECT COUNT(*) FROM pragma_table_info('clients') WHERE name='user_id'
        """))
        if result.scalar() == 0:
            # Ajouter la colonne user_id
            connection.execute(text("""
                ALTER TABLE clients ADD COLUMN user_id INTEGER REFERENCES users(id)
            """))
            print("Colonne user_id ajoutée à la table clients")
        else:
            print("La colonne user_id existe déjà dans la table clients")

if __name__ == "__main__":
    add_user_id_to_clients() 