from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    APP_HOST: str
    APP_PORT: int

    MCP_HOST: str
    MCP_PORT: int
    
    SEPAY_API_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings() # type: ignore