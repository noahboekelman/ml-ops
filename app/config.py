from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    
    app_version = 0.1
    model_version = 0.1
    environment = "dev"
    
    model_config = SettingsConfigDict(env_file=".env")
    
def get_config():
    return Config()