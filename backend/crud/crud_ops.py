from sqlalchemy.orm import Session
from models import models
from schemas import schemas
import datetime
import pytz
import logging
from services import town_services as ts

def get_towns(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Town).offset(skip).limit(limit).all()

def get_towns_initial(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.InitialWineStorage).offset(skip).limit(limit).all()

def create_town(db: Session, town: schemas.TownCreate, start_of_hour: datetime.datetime):
    db_town = models.Town(
        **town.model_dump(),
        last_update=start_of_hour
    )
    db.add(db_town)
    db.commit()
    db.refresh(db_town)
    
    initial_storage = models.InitialWineStorage(
        town_id=db_town.id,
        initial_wine_storage=db_town.wine_storage,
        initial_wine_hourly_consumption=db_town.wine_hourly_consumption,
        initial_wine_production=db_town.wine_production,
        timestamp=start_of_hour
    )
    
    db.add(initial_storage)
    db.commit()

    return db_town

def delete_town(db: Session, town_id: int):
    initial_storage = db.query(models.InitialWineStorage).filter(models.InitialWineStorage.town_id == town_id).first()
    if initial_storage:
        db.delete(initial_storage)
        # No need to commit here; committing once after all deletions is sufficient

    db_town = ts.get_town(db, town_id)
    if db_town:
        db.delete(db_town)
        db.commit()
        return True
    else:
        return False

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
        town.last_update = now  
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

def update_town_and_initial_state(db: Session, town_id: int, town_update: schemas.TownUpdate):
    town_updated = initial_state_updated = False
    current_town, initial_town_state = ts.fetch_town_and_initial_state(db, town_id)
    update_data = town_update.dict(exclude_unset=True)
    
    # Update town properties
    for key in ['town_name', 'wine_storage', 'wine_hourly_consumption', 'wine_production']:
        if key in update_data:
            setattr(current_town, key, update_data[key])
            town_updated = True

    # Update initial state for specific changes
    if any(key in update_data for key in ['wine_hourly_consumption', 'wine_production']):
        ts.update_initial_state(initial_town_state, update_data)
        initial_state_updated = True

    if town_updated:
        db.commit()
        db.refresh(current_town)

    return town_updated, initial_state_updated, current_town

def update_wine_rates(db: Session, town_id: int, updated_wine_storage: float):
    town, initial_state = ts.fetch_town_and_initial_state(db, town_id)
    
    if not town or not initial_state:
        raise ValueError("Town or initial wine storage state not found")

    elapsed_hours, discrepancy = ts.calculate_discrepancy_and_elapsed_hours(initial_state, updated_wine_storage)
    
    if elapsed_hours > 0:
        new_wine_consumption_rate = discrepancy / elapsed_hours
        town.wine_hourly_consumption = new_wine_consumption_rate
        db.commit()


















def update_town_and_initial_state2(db: Session, town_id: int, town_update: schemas.TownUpdate):
    # Existing logic to fetch and update the town record
    current_town = ts.get_town(db, town_id)
    initial_town_state = ts.get_initial_town_state(db, town_id)

    update_data = town_update.model_dump(exclude_unset=True)
    town_updated = False
    initial_state_updated = False

    # Check and update the town's current state
    if any(key in update_data for key in ['town_name', 'wine_storage', 'wine_hourly_consumption', 'wine_production']):
        for key, value in update_data.items():
            setattr(current_town, key, value)
        db.commit()
        db.refresh(current_town)
        town_updated = True

    # Check and update initial state if wine_hourly_consumption or wine_production have changed
    if 'wine_hourly_consumption' in update_data and update_data['wine_hourly_consumption'] != initial_town_state.initial_wine_hourly_consumption or \
       'wine_production' in update_data and update_data['wine_production'] != initial_town_state.initial_wine_production:
        
        initial_town_state.initial_wine_hourly_consumption = update_data.get('wine_hourly_consumption', initial_town_state.initial_wine_hourly_consumption)
        initial_town_state.initial_wine_production = update_data.get('wine_production', initial_town_state.initial_wine_production)
        initial_town_state.initial_wine_storage = update_data.get('wine_storage', initial_town_state.initial_wine_storage)
        # Optionally, update the timestamp to reflect the latest baseline update
        local_tz = pytz.timezone('Europe/Helsinki')  # Adjust to your specific timezone
        now = datetime.datetime.now(local_tz)
        start_of_hour = now.replace(minute=0, second=0, microsecond=0)
        print(f"Initial state time stamp: {start_of_hour}")
        initial_town_state.timestamp = start_of_hour
        
        db.commit()
        db.refresh(initial_town_state)
        initial_state_updated = True

    return {
        "town_updated": town_updated,
        "initial_state_updated": initial_state_updated,
        "updated_town": current_town,
        "updated_initial_state": initial_town_state
    }

def update_wine_rates2(db: Session, town_id: int, updated_wine_storage: float):
    # Fetch the town and its initial wine storage state
    town = db.query(models.Town).filter(models.Town.id == town_id).first()
    initial_state = db.query(models.InitialWineStorage).filter(models.InitialWineStorage.town_id == town_id).first()

    if not town or not initial_state:
        raise ValueError("Town or initial wine storage state not found")

    # Calculate elapsed hours since the initial timestamp
    local_tz = pytz.timezone('Europe/Helsinki')
    now = datetime.datetime.now(local_tz)
    start_of_last_hour = now.replace(minute=0, second=0, microsecond=0) - datetime.timedelta(hours=1)
    print(now)
    
    print(initial_state.timestamp)
    
    if initial_state.timestamp.tzinfo is None:
        initial_timestamp = local_tz.localize(initial_state.timestamp)
        print(initial_state.timestamp)
    else:
        initial_timestamp = initial_state.timestamp.astimezone(local_tz)


    # For testing start_of_last_hour = start_of_last_hour + timedelta(hours=5)
    print(start_of_last_hour)
    elapsed_hours = (start_of_last_hour - initial_timestamp).total_seconds() / 3600.0
    print(f"elapsed hours: {elapsed_hours}")
    if elapsed_hours <= 0:
        print("No time has elapsed or data is from the future.")
        return

    # Calculate the discrepancy in wine storage
    discrepancy = initial_state.initial_wine_storage - updated_wine_storage
    print(f"Initial state: {initial_state.initial_wine_storage} updated storage: {updated_wine_storage} discrepancy: {discrepancy}")
    # Calculate the new wine consumption rate
    new_wine_consumption_rate = discrepancy / elapsed_hours if elapsed_hours else 0

    # Update the town's wine consumption rate
    town.wine_hourly_consumption = new_wine_consumption_rate

    db.commit()

    print(f"Updated wine consumption rate for town {town_id} to {new_wine_consumption_rate} units/hour.")