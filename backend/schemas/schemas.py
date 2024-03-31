from pydantic import BaseModel

class TownBase(BaseModel):
    player_name: str
    town_name: str
    wine_storage: float
    wine_hourly_consumption: float

class TownCreate(TownBase):
    pass

class Town(TownBase):
    id: int

    class Config:
        orm_mode = True
