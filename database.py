
from sqlmodel import SQLModel,create_engine


# Create engine 
engine = create_engine("sqlite:///db/database.db",connect_args={'check_same_thread':False})

def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)