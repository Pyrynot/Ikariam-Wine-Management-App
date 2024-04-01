from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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

class TownUpdate(TownBase):
    wine_storage: Optional[float] = None
    wine_hourly_consumption: Optional[float] = None
    wine_production: Optional[float] = None
    # The Optional field allows for partial updates; fields can be omitted in the PATCH request.

class TownDelete(BaseModel):
    id: int