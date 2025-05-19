from fastapi import FastAPI
from app.models import SQLModel
from app.database import engine
from app.routes import flocks, sheep, visits, user,auth,sites


app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(flocks.router, prefix="/flocks", tags=["Flocks"])
app.include_router(sheep.router, prefix="/sheep", tags=["Sheep"])
app.include_router(visits.router, prefix="/visits", tags=["Visits"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(sites.router, prefix="/sites", tags=["Sites"])