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

models.Base.metadata.create_all(bind=engine)


scheduler = AsyncIOScheduler()


def start_scheduler():
    # Assuming update_wine_levels is adapted to work asynchronously
    # or you ensure the DB session is handled correctly for async use
    scheduler.add_job(
        func=lambda: crud_ops.update_wine_levels(db=SessionLocal()),
        trigger=CronTrigger(second=10),  # For actual use, you might want to adjust this trigger
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
    print(town.model_dump())
    db_town = crud_ops.get_town_by_name(db, town_name=town.town_name)
    if db_town:
        raise HTTPException(status_code=400, detail="Town already registered")
    return crud_ops.create_town(db=db, town=town)

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
