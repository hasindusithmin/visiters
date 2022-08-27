
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
async def create_visiter(visiter:Visiter):
    with Session(engine) as session:
        session.add(visiter)
        session.commit()
        session.refresh(visiter)
        return visiter

# Read Visiter
@app.get('/',response_model=List[Visiter],status_code=200)
async def read_visiter():
    with Session(engine) as session:
        return session.exec(select(Visiter)).all()

# Read by Id 
@app.get('/{id}',status_code=200,response_model=Visiter)
async def read_one_visiter(id:int):
    with Session(engine) as session:
        return session.get(Visiter, id)
