from datetime import datetime
from typing import Optional

import bson.errors
from bson import ObjectId
from fastapi import FastAPI, APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse

from db_models.kolekcja_sesji_model import SesjaModel, get_paczka_danych_content
from fastapi import APIRouter, Body, HTTPException

from models import db_miernik

router = APIRouter(
    prefix="/kolekcja_sesji",
    tags=["kolekcja_sesji"],
    responses={404: {"description": "Not"}}
)


@router.post("/stworze_sesje/bez_id_urzadzenia",
             response_description="Stworze sesje",
             response_model=SesjaModel)
async def create_sesje_bez_id_urzadzenia(sesja: SesjaModel = Body(...)):
    now = datetime.now()
    print("now =", now)
    dt_string = now.strftime("%d/%m/%y %H:%M:%S")
    print(f"date and time = {dt_string}")
    print(f"rozpoczecia : {sesja}")

    if hasattr(sesja, 'id'):
        delattr(sesja, 'id')
    sesja.czy_aktywna = "true"
    sesja.dlugosc_trwania_w_s = "trwa - dlugosc nieustalona"
    sesja.start_sesji = dt_string
    sesja.koniec_sesji = "nie zakonczona"
    print(f"{sesja}")
    # wrzucamy do bazy danych wraz z wygenerowanym kluczem
    db_miernik.zbior_dokumentow_sesji.insert_one(sesja.dict(by_alias=True))
    sesja = jsonable_encoder(sesja)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=sesja)


@router.get('/get_kolekcja_sesji', response_description="Zwróć wszystkie sesje")
async def get_kolekcja_sesji():
    zbior_sesji = []
    for sesja in db_miernik.zbior_dokumentow_sesji.find():
        print(sesja)
        zbior_sesji.append(SesjaModel(**sesja))
    return {"zbior sesji": zbior_sesji}


#@router.put("/stworz_paczke_danych/",
#            response_description="Dodaj do sesji paczkę danych")
#async def dodaj_sesji_paczke_danych(id_sesji: str, sesja: SesjaModel):
#    try:
#        sesja_find = db_miernik.zbior_dokumentow_sesji.find_one({"_id": ObjectId(id)})
#        if sesja_find is not None and sesja_find['czy_aktywna'] == "tak":
#            paczka_danych = get_paczka_danych_content
#            print(paczka_danych)
#            #db_miernik.zbior_dokumentow_sesji.update_one({"_id": ObjectId(id_sesji)})
#    except bson.errors.InvalidId:
#        raise HTTPException(status_code=404, detail=f"klucz id musi mieć 12 znaków !")
#    #if hasattr(paczka_danych, 'id'):
#    #    delattr(paczka_danych, 'id')
#    #db_miernik.zbior_paczek_danych.insert_one(paczka_danych.dict(by_alias=True))
#    #paczka_danych = jsonable_encoder(paczka_danych)
#    #return JSONResponse(status_code=status.HTTP_201_CREATED, content=paczka_danych)


#@router.put("/stworz_paczke_danych/",
#            response_description="Dodaj do sesji paczkę danych")
#async def dodaj_sesji_paczke_danych(id_sesji: str, sesja: SesjaModel):
#    try:
#        sesja_find = db_miernik.zbior_dokumentow_sesji.find_one({"_id": ObjectId(id)})
#        if sesja_find is not None and sesja_find['czy_aktywna'] == "tak":
#            paczka_danych = get_paczka_danych_content
#            print(paczka_danych)
#            #db_miernik.zbior_dokumentow_sesji.update_one({"_id": ObjectId(id_sesji)})
#    except bson.errors.InvalidId:
#        raise HTTPException(status_code=404, detail=f"klucz id musi mieć 12 znaków !")


@router.put("/stworz_paczke_danych/",
            response_description="Dodaj do sesji paczkę danych")
async def dodaj_sesji_paczke_danych():
        #paczka_danych = get_paczka_danych_content
        #print("paczka_danych: "+paczka_danych)
        #results = {paczka_danych}

        paczka_danych

        return results
        #db_miernik.zbior_dokumentow_sesji.update_one({"_id": ObjectId(id_sesji)})
