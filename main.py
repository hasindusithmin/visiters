
from fastapi import FastAPI,HTTPException
from database import create_db_and_tables,engine
from models import Visiter
from typing import List,Optional
from sqlmodel import Session,select
from pydantic import BaseModel

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
        visitor = session.get(Visiter, id)
        exist = True if visitor != None else False
        if not exist:
            raise HTTPException(status_code=404)
        return visitor

class VisiteR(BaseModel):
    ipv6:Optional[str] = None
    chrome:Optional[str]  = None
    port_number:Optional[int] = None
    mac_address:Optional[str] = None
    timezone:Optional[str] = None
    action:Optional[str] = None

# Update By Id 
@app.put("/{id}",status_code=202,response_model=Visiter)
async def update_visior(id:int,visiter:VisiteR):
    with Session(engine) as session:
        # Get data from DB 
        visiterInDb = session.get(Visiter, id)
        # Check If data exist or not 
        exist = True if visiterInDb != None else False
        if not exist:
            raise HTTPException(status_code=404)
        # Instance -> Dict 
        visiter = visiter.dict()
        # Update visiterInDb instance 
        for k,v in visiter.items():
            if v is None:
                continue
            exec(f'visiterInDb.{k} = "{v}"')
        # DB operations 
        session.add(visiterInDb)
        session.commit()
        session.refresh(visiterInDb)

        return visiterInDb
    
@app.delete("/{id}")
async def delete_visitor(id:int):
    with Session(engine) as session:
        visitorInDb = session.get(Visiter,id)
        if visitorInDb is None:
            raise HTTPException(status_code=404)
        session.delete(visitorInDb)
        session.commit()
        raise HTTPException(status_code=202)

