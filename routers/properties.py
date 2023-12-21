from fastapi import APIRouter, HTTPException
from typing import Literal
from database.properties_db import (
    get_properties_from_db_by_cid, 
    insert_properties_to_db_by_cid
)
from services.services import (
    get_cid_by_name,
    get_properties_by_cid
)

router = APIRouter()

@router.get("/properties_from_cid/{cid}")
async def handle_properties_from_cid(cid: int) -> dict:
    data = await get_properties_from_db_by_cid(cid=cid)
    if data:
        return data

    data = await get_properties_by_cid(cid)

    await insert_properties_to_db_by_cid(cid, data)
    return data

@router.get("/properties/{nametype}/{name}")
async def handle_properties(nametype: Literal["name", "smiles", "cid"], name: str):
    
    if nametype == "cid":
        return await handle_properties_from_cid(int(name))

    cid, status_code = await get_cid_by_name(nametype, name)

    match status_code:
        case 200:
            return await handle_properties_from_cid(cid=cid)
        case 400:
            raise HTTPException(status_code=400, detail="Проверьте, правильно ли выбран тип поиска и название.")
        case 404:
            raise HTTPException(status_code=404, detail="Нет вещества по заданному названию.")
        
