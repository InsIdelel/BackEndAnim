from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models import Sheep, Flock, User
from app.database import get_session
from app.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=Sheep)
def create_sheep(sheep: Sheep, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    flock = session.get(Flock, sheep.flock_id)
    if not flock or flock.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized.")
    session.add(sheep)
    session.commit()
    session.refresh(sheep)
    return sheep

@router.get("/", response_model=list[Sheep])
def read_sheep(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    query = select(Sheep).join(Flock).where(Flock.user_id == current_user.id)
    return session.exec(query).all()

@router.get("/{sheep_id}", response_model=Sheep)
def read_sheep_by_id(sheep_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    sheep = session.get(Sheep, sheep_id)
    if not sheep or sheep.flock.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Sheep not found or unauthorized.")
    return sheep

@router.put("/{sheep_id}", response_model=Sheep)
def update_sheep(sheep_id: int, updated_sheep: Sheep, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    db_sheep = session.get(Sheep, sheep_id)
    if not db_sheep or db_sheep.flock.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Sheep not found or unauthorized.")
    for key, value in updated_sheep.dict(exclude_unset=True).items():
        setattr(db_sheep, key, value)
    session.commit()
    session.refresh(db_sheep)
    return db_sheep

@router.delete("/{sheep_id}")
def delete_sheep(sheep_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    sheep = session.get(Sheep, sheep_id)
    if not sheep or sheep.flock.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Sheep not found or unauthorized.")
    session.delete(sheep)
    session.commit()
    return {"ok": True}
