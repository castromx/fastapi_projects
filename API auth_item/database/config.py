from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

DB_HOST_TEST = os.environ.get("DB_HOST_TEST")
DB_PORT_TEST = os.environ.get("DB_PORT_TEST")
DB_NAME_TEST = os.environ.get("DB_NAME_TEST")
DB_USER_TEST = os.environ.get("DB_USER_TEST")
DB_PASS_TEST = os.environ.get("DB_PASS_TEST")


BASE_DIR = Path(__file__).parent


class AuthJWT(BaseSettings):
    private_key_path: Path = BASE_DIR / "jwt-private.pem" 
    public_key_path: Path = BASE_DIR / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15

class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
