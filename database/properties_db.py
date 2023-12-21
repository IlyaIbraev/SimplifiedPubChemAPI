import asyncpg
import json
from config_data.config import Config, load_config

config: Config = load_config()

async def get_properties_from_db_by_cid(cid: int) -> dict:

    conn = await asyncpg.connect(
        "postgresql://{}:{}@{}/{}".format(
            config.db_config.username, 
            config.db_config.password,
            config.db_config.host, 
            config.db_config.dbname
        )
    )
    await conn.set_type_codec(
            'json',
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog'
        )
    
    data = await conn.fetchval('SELECT data FROM properties WHERE cid=$1', cid)
    return data

async def insert_properties_to_db_by_cid(cid: int, data: json) -> None:
    conn = await asyncpg.connect(
        "postgresql://{}:{}@{}/{}".format(
            config.db_config.username, 
            config.db_config.password,
            config.db_config.host, 
            config.db_config.dbname
        )
    )
    await conn.set_type_codec(
            'json',
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog'
        )
    await conn.execute('''
        INSERT INTO properties(cid, data) VALUES($1, $2::json)
    ''', cid, data)
    