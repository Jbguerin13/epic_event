from dotenv import load_dotenv
from sqlalchemy import create_engine
from models.sql_models import Base
import os

load_dotenv()
database_url = os.getenv("DATABASE_URL")

engine = create_engine(database_url, echo=True)

Base.metadata.create_all(engine)