from pydantic_settings import BaseSettings, SettingsConfigDict
import pathlib


env_path = pathlib.Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str


    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    

    model_config = SettingsConfigDict(env_file=env_path, extra="ignore")


settings = Settings()