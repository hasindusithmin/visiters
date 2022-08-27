
from fastapi import FastAPI
from database import create_db_and_tables
from models import Visiter

# Create instance -> FastAPI
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()