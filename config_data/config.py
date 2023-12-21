from dataclasses import dataclass
from environs import Env


@dataclass
class PostgreSQLConfig:
    host: str
    username: str
    password: str
    dbname: str

@dataclass
class Config:
    db_config: PostgreSQLConfig

def load_config(path: str | None = None) -> Config:

    env: Env = Env()
    env.read_env(path)

    return Config(
        db_config=PostgreSQLConfig(
            host=env('DB_HOST'),
            username=env('DB_USER'),
            password=env('DB_PASSWORD'),
            dbname=env('DB_NAME'),
        )
    )