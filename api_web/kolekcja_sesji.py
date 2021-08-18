import json
from datetime import datetime
from pprint import pprint
from typing import Optional

import bson.errors
from bson import ObjectId
from fastapi import FastAPI, APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse

from db_models.kolekcja_sesji_model import SesjaModel, PaczkaDanychModel
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
    sesja.czy_aktywna = "tak"
    sesja.dlugosc_trwania_w_s = "trwa - dlugosc nieustalona"
    sesja.start_sesji = dt_string
    sesja.koniec_sesji = "nie zakonczona"
    print(f"{sesja}")
    # wrzucamy do bazy danych wraz z wygenerowanym kluczem
    db_miernik.zbior_dokumentow_sesji.insert_one(sesja.dict(by_alias=True))
    sesja = jsonable_encoder(sesja)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=sesja)


@router.get('/get_kolekcje_sesji', response_description="Zwróć wszystkie sesje")
async def get_kolekcja_sesji():
    zbior_sesji = []
    parsed = None
    for sesja in db_miernik.zbior_dokumentow_sesji.find():
        print(sesja)
        zbior_sesji.append(SesjaModel(**sesja))
        parsed = json.load(sesja)
        print("Json dumps")
        #print(json.dumps(parsed, indent=4, sort_keys=True))
    #json.dumps(parsed, indent=4, sort_keys=True)
    return {"zbior sesji": json.dumps(parsed, indent=4, sort_keys=True)}


@router.get("/get_kolekcje_sesji/id_sesji={id_sesji}", response_description="Zwróć jedną sesję")
async def get_sesje_id(id_sesji: str):
    try:
        sesja = db_miernik.zbior_dokumentow_sesji.find_one({"_id": ObjectId(id_sesji)})
        if sesja is not None:
            print(sesja)
            sesja_element = []
            sesja_element.append(SesjaModel(**sesja))
            return {"sesja_element": sesja_element}
        raise HTTPException(status_code=404, detail=f"Sesji {id_sesji} nie znaleziono")
    except bson.errors.InvalidId:
        raise HTTPException(status_code=404, detail=f"klucz id musi mieć 12 znaków")


@router.put("/zakoncz_sesje/id_sesji={id_sesji}", response_description="Zakończ działanie sesji")
async def zakoncz_sesje(id_sesji: str):
    try:
        sesja_find = db_miernik.zbior_dokumentow_sesji.find_one({"_id": ObjectId(id_sesji)})
        #zakładam że raz zamknieta sesja nie bedzie otwierane
        if sesja_find is not None and sesja_find['czy_aktywna'] == "tak":
            now = datetime.now()
            print("now =", now)
            dt_string = now.strftime("%d/%m/%y %H:%M:%S")
            print(f"date and time = {dt_string}")
            #obliczanie dlugosci trwania sesji
            start_timestamp = datetime.strptime(sesja_find["start_sesji"], "%d/%m/%y %H:%M:%S").timestamp()
            end_timestamp=now.timestamp()
            print(f"start_timestamp {start_timestamp} end_timestamp {end_timestamp}")
            sesja_find['czy_aktywna'] = "nie"
            sesja_find['koniec_sesji'] = dt_string
            sesja_find['dlugosc_trwania_w_s'] = str(end_timestamp - start_timestamp)
            print(sesja_find)
            db_miernik.zbior_dokumentow_sesji.update_one({"_id": ObjectId(id_sesji)},
                                         {
                                             "$set":
                                             {
                                                 'czy_aktywna': sesja_find['czy_aktywna'],
                                                 'koniec_sesji': sesja_find['koniec_sesji'],
                                                 'dlugosc_trwania_w_s': sesja_find['dlugosc_trwania_w_s']
                                             }
                                         })
            sesja_element = []
            sesja_element.append(SesjaModel(**sesja_find))
            return {"sesja_element": sesja_element}
        elif sesja_find['czy_aktywna'] == "nie":
            raise HTTPException(status_code=404, detail="sprawdz czy wybrana sesja jest napewno aktywna")
        else:
            raise HTTPException(status_code=404, detail="nie ma sesji o podanym id!")
    except bson.errors.InvalidId:
        raise HTTPException(status_code=404, detail=f"klucz id musi mieć 12 znaków")


@router.delete("/delete_sesje/id_sesji={id_sesji}", response_description="Usuń sesje")
async def delete_sesja(id_sesji: str):
    delete_result = db_miernik.zbior_dokumentow_sesji.delete_one({"_id": ObjectId(id_sesji)})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=403, detail=f"Sesje {id_sesji} nie znaleziono")


@router.delete("/drop_zbior_sesji", response_description="drop sesje")  # , response_model=Wektor_Probek)
async def drop_sesje():
    db_miernik.zbior_dokumentow_sesji.drop()
    return HTTPException(status_code=404, detail=f"Kolekcje sesji nie możesz wyczyścić")


@router.put("/stworz_paczke_danych/",
            response_description="Dodaj do sesji paczkę danych")
async def dodawanie_do_aktywnej_sesji_nowej_paczki(paczka: PaczkaDanychModel = Body(...)):
    zbior_dokumentow_sesji = db_miernik.zbior_dokumentow_sesji
    liczba_aktywnych_sesji = zbior_dokumentow_sesji.find({"czy_aktywna": "tak"})
    print(liczba_aktywnych_sesji.count)
    if liczba_aktywnych_sesji.count() == 1:
        sesja_aktywna_find = zbior_dokumentow_sesji.find_one({"czy_aktywna": "tak"})
        print(sesja_aktywna_find)
        print(sesja_aktywna_find["czy_aktywna"])
        start_sesji=sesja_aktywna_find["start_sesji"]
        print(start_sesji)
        id_sesji = sesja_aktywna_find["_id"]
        print(id_sesji)
        if hasattr(paczka, 'id'):
            delattr(paczka, "id")
        paczka.czas_przyjscia_paczki = "xfa"
        paczka.kod_statusu = "casda"
        paczka.numer_seryjny_urzadzenia = "ahjo"
        zbior_dokumentow_sesji.update(
            { "_id": ObjectId(id_sesji)},
            {
              "$push":
                {
                "lista_paczek_danych":
                     {
                         "_id": "1",
                         "czas_przyjscia_paczki": paczka.czas_przyjscia_paczki,
                         "kod_status": paczka.kod_statusu,
                         "numer_seryjny_urzadzenia": paczka.numer_seryjny_urzadzenia
                         #"PackSizeName":"xyz",
                         #"UnitName":"Polska"
                     }
                }
            }
        )
