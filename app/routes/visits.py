from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models import Visit, Site, User,Flock
from app.database import get_session
from app.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=Visit)
def create_visit(visit: Visit, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    site = session.get(Site, visit.site_id)
    if not site or site.flock.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized.")
    session.add(visit)
    session.commit()
    session.refresh(visit)
    return visit

@router.get("/", response_model=list[Visit])
def read_visits(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    query = select(Visit).join(Site).join(Flock).where(Flock.user_id == current_user.id)
    return session.exec(query).all()

@router.get("/{visit_id}", response_model=Visit)
def read_visit(visit_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    visit = session.get(Visit, visit_id)
    if not visit or visit.site.flock.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Visit not found or unauthorized.")
    return visit

@router.put("/{visit_id}", response_model=Visit)
def update_visit(visit_id: int, updated_visit: Visit, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    db_visit = session.get(Visit, visit_id)
    if not db_visit or db_visit.site.flock.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Visit not found or unauthorized.")
    for key, value in updated_visit.dict(exclude_unset=True).items():
        setattr(db_visit, key, value)
    session.commit()
    session.refresh(db_visit)
    return db_visit

@router.delete("/{visit_id}")
def delete_visit(visit_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    visit = session.get(Visit, visit_id)
    if not visit or visit.site.flock.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Visit not found or unauthorized.")
    session.delete(visit)
    session.commit()
    return {"ok": True}
