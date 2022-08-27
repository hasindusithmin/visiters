from typing import Optional
from sqlmodel import SQLModel,Field


class Visiter(SQLModel,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)
    ipv6:str = Field(nullable=False)
    chrome:str = Field(nullable=False)
    port_number:Optional[int] = Field(default=None)
    mac_address:Optional[str] = Field(default=None)
    timezone:str = Field(nullable=False)
    action:str = Field(nullable=False)