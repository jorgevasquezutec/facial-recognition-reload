from pydantic_settings import BaseSettings,SettingsConfigDict

# __all__ = ("api_settings")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    HOST: str
    PORT: int
    TITLE: str
    PREFIX: str
    PASSWORD_ADMIN: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
    AUTH_ROUTE: str




api_settings =Settings(_env_file='.env', _env_file_encoding='utf-8')