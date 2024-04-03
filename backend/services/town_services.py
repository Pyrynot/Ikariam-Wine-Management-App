from datetime import datetime, timedelta, timezone
from models import models
from sqlalchemy.orm import Session
import pytz


def calculate_discrepancy_and_elapsed_hours(initial_state, updated_wine_storage):
    
    now = datetime.now(timezone.utc)
    start_of_hour = now.replace(minute=0, second=0, microsecond=0)

    initial_timestamp = initial_state.timestamp
        
    initial_timestamp = initial_timestamp.replace(tzinfo=timezone.utc)
    
    print(f"start of last hour: {start_of_hour} initial timestamp: {initial_timestamp}")
    elapsed_hours = (start_of_hour - initial_timestamp).total_seconds() / 3600.0
    discrepancy = initial_state.initial_wine_storage - updated_wine_storage

    return elapsed_hours, discrepancy


def fetch_town_and_initial_state(db: Session, town_id: int):
    town = db.query(models.Town).filter(models.Town.id == town_id).first()
    initial_state = db.query(models.InitialWineStorage).filter(models.InitialWineStorage.town_id == town_id).first()
    return town, initial_state


def update_initial_state(initial_state, update_data):
    updated = False
    for key in ['wine_hourly_consumption', 'wine_production']:
        if key in update_data and getattr(initial_state, f"initial_{key}") != update_data[key]:
            setattr(initial_state, f"initial_{key}", update_data[key])
            updated = True

    # If 'wine_storage' is part of the update, it's handled separately to ensure
    # it doesn't trigger unnecessary updates if only the storage is changing.
    if 'wine_storage' in update_data:
        initial_storage = getattr(initial_state, "initial_wine_storage")
        if initial_storage != update_data['wine_storage']:
            setattr(initial_state, "initial_wine_storage", update_data['wine_storage'])
            updated = True

    return updated


def get_town(db: Session, town_id: int):
    return db.query(models.Town).filter(models.Town.id == town_id).first()


def get_initial_town_state(db: Session, town_id: int):
    return db.query(models.InitialWineStorage).filter(models.InitialWineStorage.town_id == town_id).first()