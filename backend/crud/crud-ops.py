from sqlalchemy.orm import Session
from . import models, schemas

def get_town(db: Session, town_id: int):
    return db.query(models.Town).filter(models.Town.id == town_id).first()

def get_town_by_name(db: Session, town_name: str):
    return db.query(models.Town).filter(models.Town.town_name == town_name).first()

def get_towns(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Town).offset(skip).limit(limit).all()

def create_town(db: Session, town: schemas.TownCreate):
    db_town = models.Town(**town.dict())
    db.add(db_town)
    db.commit()
    db.refresh(db_town)
    return db_town

def update_town(db: Session, town_id: int, updates: schemas.TownCreate):
    db_town = get_town(db, town_id)
    if db_town:
        update_data = updates.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_town, key, value)
        db.commit()
        db.refresh(db_town)
    return db_town

def delete_town(db: Session, town_id: int):
    db_town = get_town(db, town_id)
    if db_town:
        db.delete(db_town)
        db.commit()
    return db_town
