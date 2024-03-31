from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud_ops, models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/towns/", response_model=List[schemas.Town])
def read_towns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    towns = crud_ops.get_towns(db, skip=skip, limit=limit)
    return towns

@app.post("/towns/", response_model=schemas.Town)
def create_town(town: schemas.TownCreate, db: Session = Depends(database.get_db)):
    db_town = crud_ops.get_town_by_name(db, town_name=town.town_name)
    if db_town:
        raise HTTPException(status_code=400, detail="Town already registered")
    return crud_ops.create_town(db=db, town=town)