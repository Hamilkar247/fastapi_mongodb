from fastapi import FastAPI, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse
from models_miernik import UzytkownikModel, db_miernik\
    , StudentModel, UpdateStudentModel, PaczkaDanychModel
from models_miernik import SesjaModel
from datetime import datetime
from fastapi import APIRouter


router = APIRouter(
    prefix="/uzytkownicy",
    tags=["uzytkownicy"],
    responses={404: {"description": "Not"}}
)


@router.post('/uzytkownicy/')
async def create_uzytkownik(uzytkownik: UzytkownikModel):
    if hasattr(uzytkownik, 'id'):
        delattr(uzytkownik, 'id')
    ret = db_miernik.users.insert_one(uzytkownik.dict(by_alias=True))
    uzytkownik.id = ret.inserted_id
    return {'uzytkownik': uzytkownik}


@router.get('/user/')
async def get_users():
    uzytkownicy = []
    for uzytkownik in db_miernik.users.find():
        uzytkownicy.append(UzytkownikModel(**uzytkownik))
    return {'uzytkownicy': uzytkownicy}
