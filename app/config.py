from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    
    app_version: str = "v0.1"
    model_version: str = "v0.1"
    environment: str = "dev"

    model_config = SettingsConfigDict(env_file=".env", protected_namespaces=())
    
def get_config():
    return Config()