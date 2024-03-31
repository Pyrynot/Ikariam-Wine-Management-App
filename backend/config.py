from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./wine_game.db"

    class Config:
        env_file = ".env"

settings = Settings()
