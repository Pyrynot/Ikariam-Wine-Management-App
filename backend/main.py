from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from crud import crud_ops
from schemas import schemas
from models import models
from database import engine, get_db, SessionLocal
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import datetime
import pytz
import logging

logging.basicConfig(filename='wine_updates.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

models.Base.metadata.create_all(bind=engine)


scheduler = AsyncIOScheduler()


def start_scheduler():
    # Assuming update_wine_levels is adapted to work asynchronously
    # or you ensure the DB session is handled correctly for async use
    scheduler.add_job(
        func=lambda: crud_ops.update_wine_levels(db=SessionLocal()),
        trigger=CronTrigger(hour='*', minute=0, second=0),  # For actual use, you might want to adjust this trigger
    )
    scheduler.start()

    

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()  # Start the scheduler
    yield  # Yield control back to FastAPI
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/towns/", response_model=List[schemas.Town])
def read_towns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    towns = crud_ops.get_towns(db, skip=skip, limit=limit)
    return towns

@app.post("/towns/", response_model=schemas.Town)
def create_town(town: schemas.TownCreate, db: Session = Depends(get_db)):

    local_tz = pytz.timezone('Europe/Helsinki')  # Adjust to your specific timezone
    now = datetime.datetime.now(local_tz)
    start_of_hour = now.replace(minute=0, second=0, microsecond=0)

    # Create a new town with last_update set to the start of the hour
    db_town = models.Town(
        player_name=town.player_name,
        town_name=town.town_name,
        wine_storage=town.wine_storage,
        wine_hourly_consumption=town.wine_hourly_consumption,
        wine_production=town.wine_production,
        last_update=start_of_hour  # Manually set last_update
    )

    db.add(db_town)
    db.commit()
    db.refresh(db_town)

    return db_town

@app.post("/towns/transfer/")
def transfer_wine(transfer_request: schemas.TownTransfer, db: Session = Depends(get_db)):
    # Validate towns belong to the same player and perform the transfer
    result = crud_ops.transfer_wine_between_towns(db=db, transfer_request=transfer_request)
    if not result:
        raise HTTPException(status_code=400, detail="Transfer failed")
    return {"message": "Transfer successful"}

@app.get("/force-update/")
def force_update_wine_levels(db: Session = Depends(get_db)):
    crud_ops.update_wine_levels(db)
    return {"message": "Wine levels updated"}

@app.put("/towns/{town_id}/", response_model=schemas.Town)
def update_town(town_id: int, town_update: schemas.TownUpdate, db: Session = Depends(get_db)):
    # Update the town in the database using CRUD operations
    updated_town = crud_ops.update_town(db, town_id=town_id, town_update=town_update)
    if not updated_town:
        raise HTTPException(status_code=404, detail="Town not found")
    return updated_town

@app.delete("/towns/{town_id}/")
def delete_town(town_id: int, db: Session = Depends(get_db)):
    # Delete the town from the database
    result = crud_ops.delete_town(db, town_id=town_id)
    if not result:
        raise HTTPException(status_code=404, detail="Town not found")
    return {"message": "Town deleted successfully"}
