from datetime import datetime

import bson
from bson import ObjectId
from fastapi import FastAPI, Body, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse
from models_miernik import  db_miernik, PaczkaDanychModel

router = APIRouter(
    prefix="/paczki_danych",
    tags=["paczki_danych"],
    responses={404: {"description": "Not"}}
)


@router.post("/stworz_paczke_danych/bez_id_urzadzenia"
    , response_description="Stwórz paczkę danych"
    , response_model=PaczkaDanychModel)
async def create_paczke_danych(paczka_danych: PaczkaDanychModel = Body(...)):
    if hasattr(paczka_danych, 'id'):
        delattr(paczka_danych, 'id')
    db_miernik.zbior_paczek_danych.insert_one(paczka_danych.dict(by_alias=True))
    paczka_danych = jsonable_encoder(paczka_danych)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=paczka_danych)


@router.post("/stworz_paczke_danych/id_urzadzenia={id_urzadzenia}"
    , response_description="Stwórz paczkę danych"
    , response_model=PaczkaDanychModel)
async def create_paczke_danych(id_urzadzenia: str, paczka_danych: PaczkaDanychModel = Body(...)):
    try:
        now = datetime.now()
        print("now =", now)
        dt_string = now.strftime("%d/%m/%y %H:%M:%S")
        print(f"date and time = {dt_string}")

        urzadzenie_result = db_miernik.zbior_urzadzen.find_one(ObjectId(id_urzadzenia))
        if urzadzenie_result is None:
            print("Nie znaleziono urzadzenia w zbiorze")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Nie znaleziono urządzenia o tym id")
        else:
            if hasattr(paczka_danych, 'id'):
                delattr(paczka_danych, 'id')
            paczka_danych.id_urzadzenia = id_urzadzenia
            paczka_danych.czas_paczki = dt_string
            db_miernik.zbior_paczek_danych.insert_one(paczka_danych.dict(by_alias=True))
            paczka_danych = jsonable_encoder(paczka_danych)
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=paczka_danych)
    except bson.errors.InvalidId:
        raise HTTPException(status_code=404, detail=f"klucz id musi mieć 12 znaków")


@router.get('/get_zbior_paczek_danych', response_description="Zwróć wszystkie paczki danych")
async def get_paczki_danych():
    zbior_paczek_danych = []
    for paczka_danych in db_miernik.zbior_paczek_danych.find():
        zbior_paczek_danych.append(PaczkaDanychModel(**paczka_danych))
    return {'zbior_paczek_danych': zbior_paczek_danych}


@router.get("/get_paczke_danych/id={id}", response_description="Zwroc jedna paczke danych")#, response_model=Wektor_Probek)
async def get_id_paczke_danych(id: str):
    if (paczki_danych := db_miernik.zbior_paczek_danych.find_one({"_id": id})) is not None: #usuwam await przez db_miernik
        return paczki_danych
    raise HTTPException(status_code=404, detail=f"Paczki danych o {id} nie znaleziono")


@router.delete("/delete_paczke_danych/id_paczki_danych={id}", response_description="Usuń paczki danych")
async def delete_paczki_danych(id: str):
    ## DO DODANIA - do zastanowienia sie czy to powinno być usuniecie kaskadowa
    delete_result = db_miernik.zbior_paczek_danych.delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=403, detail=f"Paczki danych o {id} nie znaleziono")


@router.delete("/drop_paczki_danych/", response_description="drop paczki danych")#, response_model=Wektor_Probek)
async def drop_paczki_danych():
    db_miernik.zbior_paczek_danych.drop()
    return HTTPException(status_code=404, detail=f"Kolekcja wektorów próbek nie możesz wyczyścić")

