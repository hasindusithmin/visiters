
from fastapi import FastAPI,HTTPException
from database import create_db_and_tables,engine
from models import Visiter
from typing import List
from sqlmodel import Session,select

# Create instance -> FastAPI
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Create Visiter
@app.post("/",status_code=201,response_model=Visiter)
def create_visiter(visiter:Visiter):
    with Session(engine) as session:
        session.add(visiter)
        session.commit()
        session.refresh(visiter)
        return visiter
