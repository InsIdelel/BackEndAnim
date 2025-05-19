from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models import Site, Flock, User
from app.database import get_session
from app.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=Site)
def create_site(site: Site, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    flock = session.get(Flock, site.flock_id)
    if not flock or flock.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized.")
    session.add(site)
    session.commit()
    session.refresh(site)
    return site

@router.get("/", response_model=list[Site])
def read_sites(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    query = select(Site).join(Flock).where(Flock.user_id == current_user.id)
    return session.exec(query).all()

@router.get("/{site_id}", response_model=Site)
def read_site(site_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    site = session.get(Site, site_id)
    if not site or site.flock.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Site not found or unauthorized.")
    return site

@router.put("/{site_id}", response_model=Site)
def update_site(site_id: int, updated_site: Site, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    db_site = session.get(Site, site_id)
    if not db_site or db_site.flock.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Site not found or unauthorized.")
    for key, value in updated_site.dict(exclude_unset=True).items():
        setattr(db_site, key, value)
    session.commit()
    session.refresh(db_site)
    return db_site

@router.delete("/{site_id}")
def delete_site(site_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    site = session.get(Site, site_id)
    if not site or site.flock.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Site not found or unauthorized.")
    session.delete(site)
    session.commit()
    return {"ok": True}
