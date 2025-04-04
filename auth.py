import os
import jwt
import datetime
from dotenv import load_dotenv
from database import SessionLocal
from models.sql_models import User

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    """create access token JWT with expiration time"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta #try avec now()
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """verify and encode token
    return payload if token is valid else return an error"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return "Token expired"
    except jwt.InvalidTokenError:
        return "Invalid token"
    except Exception as e:
        return str(e)
    
def authenticate_user(username: str, password: str):
    """authenticate user"""
    session = SessionLocal()
    try:
        print(f"Tentative d'authentification pour l'utilisateur: {username}")
        user = session.query(User).filter(User.username == username).first()
        if not user:
            print("Utilisateur non trouvé")
            return None
        if not user.verify_password(password):
            print("Mot de passe incorrect")
            return None
        print(f"Utilisateur authentifié avec succès: {user.username} (ID: {user.id})")
        return user
    except Exception as e:
        print(f"Erreur lors de l'authentification: {str(e)}")
        return None
    finally:
        session.close()