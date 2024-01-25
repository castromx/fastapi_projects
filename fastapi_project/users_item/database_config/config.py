from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent

# Файл конфігурацій налаштувань

class DbSettings(BaseSettings):
    echo: bool = True

class AuthJWT(BaseSettings):
    private_key_path: Path = BASE_DIR / "jwt-private.pem" 
    public_key_path: Path = BASE_DIR / "jwt-public.pem"
    algorithm: str = "RS256" # Алгоритм хешування
    access_token_expire_minutes: int = 15 # Час життя токену

class Settings(BaseSettings):
    # Створюємо клас основних налаштувань
    db: DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()

# І передаємо його в екземпляр
settings = Settings()
