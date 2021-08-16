from datetime import datetime

import bson
from bson import ObjectId
from fastapi import FastAPI, Body, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse
from models_miernik import  db_miernik, WartoscPomiaruSensora


router = APIRouter(
    prefix="/wartosci_pomiaru_sensora",
    tags=["wartosci_pomiaru_sensora"],
    responses={404: {"description": "Not"}}
)


@router.post("/stworz_wartosci/bez_id_paczki",
             response_description="Stworz wartosci danych",
             response_model=WartoscPomiaruSensora)
async def create_wartosc_pomiaru_sensora(wartosc_pomiaru_sensora: WartoscPomiaruSensora = Body(...)):
    if hasattr(wartosc_pomiaru_sensora, "id"):
        delattr(wartosc_pomiaru_sensora, "id")
    db_miernik.zbior_wartosci_pomiarow_sensorow.insert_one(wartosc_pomiaru_sensora.dict(by_alias=True))
    wartosc_pomiaru_sensora = jsonable_encoder(wartosc_pomiaru_sensora)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=wartosc_pomiaru_sensora)


@router.post("/stworz_wartosci/id_paczki_danych={id_paczki_danych}",
             response_description="Stwórz wartości dla czujnika",
             response_model=WartoscPomiaruSensora)
async def create_paczka_danych(id_paczki_danych: str, wartosc_pomiaru_sensora: WartoscPomiaruSensora = Body(...)):
    try:
        paczka_danych_result = db_miernik.zbior_paczek_danych.find_one(ObjectId(id_paczki_danych))
        if paczka_danych_result is None:
            print(f"Nie znaleziono paczki danych w zbiorze o id {id_paczki_danych}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Nie znaleziono paczki o id {id_paczki_danych}")
        else:
            if hasattr(wartosc_pomiaru_sensora, "id"):
                delattr(wartosc_pomiaru_sensora, "id")
            print(f"wartosc_pomiaru_sensora: {wartosc_pomiaru_sensora}")
            wartosc_pomiaru_sensora.id_paczki_danych = id_paczki_danych
            db_miernik.zbior_wartosci_pomiarow_sensorow.insert_one(wartosc_pomiaru_sensora.dict(by_alias=True))
            wartosc_pomiaru_sensora = jsonable_encoder(wartosc_pomiaru_sensora)
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=wartosc_pomiaru_sensora)
    except bson.errors.InvalidId:
        raise HTTPException(status_code=404, detail=f"klucz id musi mieć 12 znakow!")


@router.get("/get_wartosci_pomiaru_sensora", response_description="Zwróć wszystkie wartości")
async def get_wartosci_pomiaru_sensora():
    wartosci_pomiaru_sensora_zbior = []
    for wartosc_pomiaru in db_miernik.zbior_wartosci_pomiarow_sensorow.find():
        print(wartosc_pomiaru)
        wartosci_pomiaru_sensora_zbior.append(WartoscPomiaruSensora(**wartosc_pomiaru))
    return {"wartosci_pomiaru_sensora:": wartosci_pomiaru_sensora_zbior}


@router.get("/get_wartosci_pomiaru_sensora/id={id}", response_description="Zwróć jedna wartosc pomiaru sensora")
async def get_wartosci_pomiaru_sensora_id(id: str):
    try:
        wartosc_pomiaru = db_miernik.zbior_wartosci_pomiarow_sensorow.find_one({"_id": ObjectId(id)})
        if wartosc_pomiaru is not None:
            print(wartosc_pomiaru)
            wartosc_pomiaru_element = []
            wartosc_pomiaru_element.append(WartoscPomiaruSensora(**wartosc_pomiaru))
            return {"wartosc_pomiaru_element": wartosc_pomiaru_element}
        raise HTTPException(status_code=404, detail=f"Wartosc pomiaru sensora o dla id {id} nie znaleziono")
    except bson.errors.InvalidId:
        raise HTTPException(status_code=404, detail=f"klucz id musi mieć 12 znaków")


@router.delete("/delete_wartosc_pomiaru/id={id}", response_description="Usuń wartość pomiaru")
async def delete_wartosc_pomiaru(id: str):
    delete_result = db_miernik.zbior_wartosci_pomiarow_sensorow.delete_one({"_id": ObjectId(id)})
    print(delete_result)
    if delete_result.deleted_count == 1: ## podejrzewam że delete result - to podaje 1 gdy przy usunieciu coś nie poszło
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/drop_wartosci_pomiarow_sensorow", response_description="drop sesje")  # , response_model=Wektor_Probek)
async def drop_wartosci_pomiarowe_sensorow():
    db_miernik.zbior_wartosci_pomiarow_sensorow.drop()
    return HTTPException(status_code=404, detail=f"Kolekcje sesji nie możesz wyczyścić")
