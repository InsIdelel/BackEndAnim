from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models import User, UserCreate, UserRead
from app.database import get_session
from app.routes.auth import get_current_user
import bcrypt

router = APIRouter()

@router.post("/", response_model=UserRead)
def create_user(user_create: UserCreate, session: Session = Depends(get_session)):
    # Vérifie si l'email est déjà utilisé
    existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash du mot de passe
    hashed_password = bcrypt.hashpw(user_create.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # Crée le nouvel utilisateur
    user = User(
        name=user_create.name,
        email=user_create.email,
        password_hash=hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
