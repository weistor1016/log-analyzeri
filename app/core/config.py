from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    environment: str = "development"
    log_level: str = "INFO"

    model_config = ConfigDict(env_file=".env")

settings = Settings()