from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    
    app_version: str = "0.1"
    model_version: str = "v0.2"
    environment: str = "dev"

    model_config = SettingsConfigDict(env_file=".env")
    
def get_config():
    return Config()