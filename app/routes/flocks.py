from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models import Flock, User
from app.database import get_session
from app.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=Flock)
def create_flock(flock: Flock, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    flock.user_id = current_user.id
    session.add(flock)
    session.commit()
    session.refresh(flock)
    return flock

@router.get("/", response_model=list[Flock])
def read_flocks(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return session.exec(select(Flock).where(Flock.user_id == current_user.id)).all()

@router.get("/{flock_id}", response_model=Flock)
def read_flock(flock_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    flock = session.get(Flock, flock_id)
    if not flock or flock.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Flock not found or unauthorized.")
    return flock

@router.put("/{flock_id}", response_model=Flock)
def update_flock(flock_id: int, updated_flock: Flock, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    flock = session.get(Flock, flock_id)
    if not flock or flock.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Flock not found or unauthorized.")
    for key, value in updated_flock.dict(exclude_unset=True).items():
        setattr(flock, key, value)
    session.commit()
    session.refresh(flock)
    return flock

@router.delete("/{flock_id}")
def delete_flock(flock_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    flock = session.get(Flock, flock_id)
    if not flock or flock.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Flock not found or unauthorized.")
    session.delete(flock)
    session.commit()
    return {"ok": True}
