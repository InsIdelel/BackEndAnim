from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password_hash: str
    flocks: List["Flock"] = Relationship(back_populates="user")


class Flock(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="flocks")
    sites: List["Site"] = Relationship(back_populates="flock")
    sheep: List["Sheep"] = Relationship(back_populates="flock")


class Site(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: str  # 'vide' ou 'complet'
    notes: Optional[str]
    latitude: float
    longitude: float
    flock_id: int = Field(foreign_key="flock.id")
    flock: Optional[Flock] = Relationship(back_populates="sites")
    visits: List["Visit"] = Relationship(back_populates="site")


class Sheep(SQLModel, table=True):
    idBoucle: str = Field(primary_key=True)  # boucle électronique
    race: str
    sexe: str
    age: int
    couleur: str
    flock_id: int = Field(foreign_key="flock.id")
    flock: Optional[Flock] = Relationship(back_populates="sheep")


class Visit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date
    notes: Optional[str]
    site_id: int = Field(foreign_key="site.id")
    site: Optional[Site] = Relationship(back_populates="visits")

class UserCreate(SQLModel):
    name: str
    email: str
    password: str

class UserRead(SQLModel):
    id: int
    name: str
    email: str
