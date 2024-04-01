from fastapi import FastAPI
from crud import crud_ops
from models import models
from database import engine, SessionLocal
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import logging
from routers import towns_router

logging.basicConfig(filename='wine_updates.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

models.Base.metadata.create_all(bind=engine)

scheduler = AsyncIOScheduler()

def start_scheduler():
    scheduler.add_job(
        func=lambda: crud_ops.update_wine_levels(db=SessionLocal()),
        trigger=CronTrigger(hour='*', minute=0, second=0), # Run every hour, on the hour
    )
    scheduler.start()

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()  
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

app.include_router(towns_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)



