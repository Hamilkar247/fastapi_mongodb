from bson import ObjectId
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
    ret = db_miernik.zbior_uzytkownikow.insert_one(uzytkownik.dict(by_alias=True))
    uzytkownik.id = ret.inserted_id
    return {'uzytkownik': uzytkownik}


@router.get('/user/')
async def get_uzytkownik():
    zbior_uzytkownikow = []
    for uzytkownik in db_miernik.zbior_uzytkownikow.find():
        zbior_uzytkownikow.append(UzytkownikModel(**uzytkownik))
    return {'uzytkownicy': zbior_uzytkownikow}


@router.get("/{id}", response_description="Zwroc jednego użytkownika")#, response_model=Wektor_Probek)
async def get_uzytkownika_id(id: str):
    uzytkownik = db_miernik.zbior_uzytkownikow.find_one({"_id": ObjectId(id)})
    if uzytkownik is not None:
        uzytkownik_element = []
        uzytkownik_element.append(UzytkownikModel(**uzytkownik))
        return {"sensor_element": uzytkownik_element}
    raise HTTPException(status_code=404, detail=f"Sensor o {id} nie znaleziono")
