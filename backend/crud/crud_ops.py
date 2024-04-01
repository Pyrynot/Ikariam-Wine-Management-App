from sqlalchemy.orm import Session
from models import models
from schemas import schemas
import datetime
import pytz
import logging

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

def update_town(db: Session, town_id: int, town_update: schemas.TownUpdate):
    db_town = get_town(db, town_id)
    if db_town:
        update_data = town_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_town, key, value)
        db.commit()
        db.refresh(db_town)
        return db_town
    else:
        raise ValueError(f"Town with id {town_id} does not exist")

def delete_town(db: Session, town_id: int):
    db_town = get_town(db, town_id)
    if db_town:
        db.delete(db_town)
        db.commit()
        return db_town
    else:
        raise ValueError(f"Town with id {town_id} does not exist")

def update_wine_levels(db: Session):
    towns = db.query(models.Town).all()
    local_tz = pytz.timezone('Europe/Helsinki')  # Adjust to your specific timezone
    now = datetime.datetime.now(local_tz)
    for town in towns:
        # Ensure town.last_update is offset-aware in the same timezone
        if town.last_update.tzinfo is None:
            # If town.last_update is naive, make it aware using the local timezone
            town_last_update_aware = local_tz.localize(town.last_update)
        else:
            # Otherwise, convert it to the local timezone
            town_last_update_aware = town.last_update.astimezone(local_tz)
        elapsed_time = (now - town_last_update_aware).total_seconds() / 3600

        # Net wine change calculation
        net_wine_change = (town.wine_production - town.wine_hourly_consumption) * elapsed_time
        # Ensure that the wine storage reflects production and consumption accurately
        town.wine_storage += net_wine_change  # Directly apply net change
        logging.info(f"Player name {town.player_name}. Town name {town.town_name}. Town ID {town.id}: Wine storage updated. {abs(net_wine_change)} wine units {'removed' if net_wine_change < 0 else 'added'}.")

        
        # Update town.last_update to be offset-aware
        # Ensure wine storage does not drop below zero
        town.wine_storage = max(town.wine_storage, 0)

        # Update the last_update to now (make sure it's appropriately timezoned)
        town.last_update = now  # Convert back to UTC for consistency in storage
    db.commit()

def transfer_wine_between_towns(db: Session, transfer_request: schemas.TownTransfer) -> bool:
    # Fetch both towns
    source_town = db.query(models.Town).filter(models.Town.town_name == transfer_request.source_town_name, models.Town.player_name == transfer_request.player_name).first()
    destination_town = db.query(models.Town).filter(models.Town.town_name == transfer_request.destination_town_name, models.Town.player_name == transfer_request.player_name).first()

    if not source_town or not destination_town or source_town.wine_storage < transfer_request.wine_amount:
        return False  # Validation failed

    # Perform the transfer
    source_town.wine_storage -= transfer_request.wine_amount
    destination_town.wine_storage += transfer_request.wine_amount

    # Save changes
    db.commit()
    return True

