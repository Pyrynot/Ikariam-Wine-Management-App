from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from crud import crud_ops
from schemas import schemas
from database import get_db
import datetime
import pytz

router = APIRouter()

@router.get("/towns/", response_model=List[schemas.Town])
def read_towns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    towns = crud_ops.get_towns(db, skip=skip, limit=limit)
    return towns


@router.get("/towns/initial/", response_model=List[schemas.InitialData])
def read_initial_towns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    towns = crud_ops.get_towns_initial(db, skip=skip, limit=limit)
    return towns


@router.post("/towns/", response_model=schemas.Town)
def create_town(town: schemas.TownCreate, db: Session = Depends(get_db)):

    local_tz = pytz.timezone('Europe/Helsinki')  # Adjust to your specific timezone
    now = datetime.datetime.now(local_tz)
    start_of_hour = now.replace(minute=0, second=0, microsecond=0)

    db_town = crud_ops.create_town(db, town, start_of_hour)
    if not db_town:
        raise HTTPException(status_code=400, detail="Error creating town")
    return db_town


@router.post("/towns/transfer/")
def transfer_wine(transfer_request: schemas.TownTransfer, db: Session = Depends(get_db)):
    if not crud_ops.transfer_wine_between_towns(db, transfer_request):
        raise HTTPException(status_code=400, detail="Transfer failed")
    return {"message": "Transfer successful"}

@router.get("/force-update/")
def force_update_wine_levels(db: Session = Depends(get_db)):
    crud_ops.update_wine_levels(db)
    return {"message": "Wine levels updated"}


@router.put("/towns/{town_id}/", response_model=schemas.Town)
def update_town(town_id: int, town_update: schemas.TownUpdate, db: Session = Depends(get_db)):
    town_updated, initial_state_updated, updated_town = crud_ops.update_town_and_initial_state(db, town_id, town_update)
    
    if not updated_town:
        raise HTTPException(status_code=404, detail="Town not found after update")
    
    if town_updated and not initial_state_updated:
        crud_ops.update_wine_rates(db, town_id, town_update.wine_storage)
    
    db.refresh(updated_town)  
    return updated_town


@router.delete("/towns/{town_id}/")
def delete_town(town_id: int, db: Session = Depends(get_db)):
    if not crud_ops.delete_town(db, town_id=town_id):
        raise HTTPException(status_code=404, detail="Town not found")
    return {"message": "Town deleted successfully"}
















@router.put("/townss/{town_id}/", response_model=schemas.Town)
def update_town(town_id: int, town_update: schemas.TownUpdate, db: Session = Depends(get_db)):
    update_data = town_update.model_dump(exclude_unset=True)
    print(f"update_data: {update_data}")
    
    # Call the new function that updates the town and checks/updates initial state as needed
    result = crud_ops.update_town_and_initial_state(db, town_id, town_update)
    
    # Extract the flags and updated instances from the result
    town_updated = result["town_updated"]
    initial_state_updated = result["initial_state_updated"]
    updated_town = result["updated_town"]
    updated_initial_state = result["updated_initial_state"]

    new_storage_input = update_data.get("wine_storage")

    if initial_state_updated == False:
        crud_ops.update_wine_rates(db, town_id, new_storage_input)
    # For debugging, print out what was updated
    print(f"Town updated: {town_updated}")
    print(f"Initial state updated: {initial_state_updated}")
    print(f"Updated town: {updated_town.wine_storage}, {updated_town.wine_hourly_consumption}, {updated_town.wine_production}")
    print(f"Updated initial state: {updated_initial_state.initial_wine_storage}, {updated_initial_state.initial_wine_hourly_consumption}, {updated_initial_state.initial_wine_production}")

    if not updated_town:
        raise HTTPException(status_code=404, detail="Town not found after update")
    
    # If you want to return the town with potentially updated initial rates, make sure your schema can handle it
    # You may need to refresh the town instance or adjust the returned schema to reflect any changes
    db.refresh(updated_town)  # Refresh the instance to ensure it's up-to-date

    return updated_town