from sqlalchemy import Column, Integer, String, Float, create_engine, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func

SQLALCHEMY_DATABASE_URL = "sqlite:///./wine_game.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Town(Base):
    __tablename__ = "towns"

    id = Column(Integer, primary_key=True, index=True)
    player_name = Column(String, index=True)
    town_name = Column(String, index=True)
    wine_storage = Column(Float)
    wine_hourly_consumption = Column(Float)
    wine_production = Column(Float, default=0)
    last_update = Column(DateTime(timezone=True), server_default=func.now())
    
    initial_storage = relationship("InitialWineStorage", back_populates="town", uselist=False)

class InitialWineStorage(Base):
    __tablename__ = "initial_wine_storage"
    
    id = Column(Integer, primary_key=True, index=True)
    town_id = Column(Integer, ForeignKey('towns.id'))
    initial_wine_storage = Column(Float)
    initial_wine_hourly_consumption = Column(Float)
    initial_wine_production = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    town = relationship("Town", back_populates="initial_storage")

    #delete initialwinestorage, and implement tracking with wine press level and base consumption
    #implement daily login bonus tracking