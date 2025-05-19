from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# URL de connexion à la base de données (PostgreSQL dans cet exemple)
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set in the environment or .env file")

# Création du moteur de base de données
engine = create_engine(DATABASE_URL, echo=True)

# Fonction pour récupérer une session de base de données
def get_session() -> Session:
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session()

# Fonction pour créer la base de données et les tables
def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)
