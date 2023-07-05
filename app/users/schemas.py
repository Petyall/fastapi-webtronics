from typing import Optional
from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str


class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    first_name: str
    last_name: str


class UserLogin(UserBase):
    password: str

class UserUpdate(UserBase):
    first_name: Optional[str]
    last_name: Optional[str]

class User(UserBase):
    id: int
    role: str

    class Config:
        orm_mode = True