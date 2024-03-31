from pydantic import BaseModel
from datetime import datetime

class TownBase(BaseModel):
    player_name: str
    town_name: str
    wine_storage: float
    wine_hourly_consumption: float
    wine_production: float = 0  # Default to 0 if not specified

class TownCreate(TownBase):
    pass

class Town(TownBase):
    id: int
    last_update: datetime

    class Config:
        orm_mode = True

class TownTransfer(BaseModel):
    player_name: str
    source_town_name: str
    destination_town_name: str
    wine_amount: float