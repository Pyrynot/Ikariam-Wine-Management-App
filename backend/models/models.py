from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./wine_game.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Town(Base):
    __tablename__ = "towns"

    id = Column(Integer, primary_key=True, index=True)
    player_name = Column(String, index=True)
    town_name = Column(String, unique=True, index=True)
    wine_storage = Column(Float)
    wine_hourly_consumption = Column(Float)
