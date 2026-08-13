from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    full_name:str|None=None
    phone:str|None=None
    role:str="user"

class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    email:str|None=None
    password:str|None=None
    full_name:str|None=None
    phone:str|None=None