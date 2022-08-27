
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
@app.post("/",response_class=List[Visiter],status_code=200)
async def create_visiter(visiter:Visiter):
    try:
        with Session(bind=engine) as session:
            return session.exec(select(visiter)).all()
    except:
        raise HTTPException(status_code=400)
