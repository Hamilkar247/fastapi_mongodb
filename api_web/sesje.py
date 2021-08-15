import time

import bson
from bson import ObjectId
from fastapi import FastAPI, APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse
from models_miernik import UzytkownikModel, db_miernik, \
    StudentModel, UpdateStudentModel, PaczkaDanychModel
from models_miernik import SesjaModel
from datetime import datetime

router = APIRouter(
    prefix="/sesje",
    tags=["sesje"],
    responses={404: {"description": "Not"}}
)


@router.post("/stworz_sesje/bez_id_urzadzenia", response_description="Stworz sesje bez id urzadzenia",
             response_model=SesjaModel)
async def create_sesja_bez_id_urzadzenia(sesja: SesjaModel = Body(...)):
    now = datetime.now()
    print("now =", now)
    dt_string = now.strftime("%d/%m/%y %H:%M:%S")
    print(f"date and time = {dt_string}")
    print(f"rozpoczecia : {sesja}")

    if hasattr(sesja, 'id'):
        delattr(sesja, 'id')
    sesja.czy_aktywna = "true"
    sesja.dlugosc_trwania = "trwa - dlugosc nieustalona"
    sesja.start_sesji = dt_string
    sesja.koniec_sesji = "nie zakonczona"
    print(f"{sesja}")
    # wrzucamy do bazy danych wraz z wygenerowanym kluczem
    db_miernik.zbior_sesji.insert_one(sesja.dict(by_alias=True))
    sesja = jsonable_encoder(sesja)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=sesja)


@router.post("/stworz_sesje/id_urzadzenia={id_urzadzenia}", response_description="Stworz sesje",
             response_model=SesjaModel)
async def create_sesja(id_urzadzenia: str, sesja: SesjaModel = Body(...)):
    now = datetime.now()
    print("now =", now)
    dt_string = now.strftime("%d/%m/%y %H:%M:%S")
    print(f"date and time = {dt_string}")
    print(f"rozpoczecia : {sesja}")
    print(f"id_urzadzenia: " + id_urzadzenia)

    urzadzenie_result = db_miernik.zbior_urzadzen.find_one(ObjectId(id_urzadzenia))
    if urzadzenie_result is None:
        print("Nie znaleziono urzadzenia w zbiorze")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Nie znaleziono urządzenia o tym id")
    else:
        if hasattr(sesja, 'id'):
            delattr(sesja, 'id')
        sesja.id_urzadzenia = id_urzadzenia
        sesja.czy_aktywna = "tak"
        sesja.dlugosc_trwania_w_s = "trwa"
        sesja.start_sesji = dt_string
        sesja.koniec_sesji = "nie zakonczona"
        print(f"{sesja}")
        # wrzucamy do bazy danych wraz z wygenerowanym kluczem
        db_miernik.zbior_sesji.insert_one(sesja.dict(by_alias=True))
        sesja = jsonable_encoder(sesja)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=sesja)


@router.get('/get_zbior_sesji', response_description="Zwroc wszystkie sesje")
async def get_zbior_sesji():
    sesja_zbior = []
    for sesja in db_miernik.zbior_sesji.find():
        print(sesja)
        sesja_zbior.append(SesjaModel(**sesja))
    return {"sesja_zbior": sesja_zbior}


@router.get("/get_sesje/id={id}", response_description="Zwróć jedną sesję")
async def get_sesje_id(id: str):
    try:
        sesja = db_miernik.zbior_sesji.find_one({"_id": ObjectId(id)})
        if sesja is not None:
            print(sesja)
            sesja_element = []
            sesja_element.append(SesjaModel(**sesja))
            return {"sesja_element": sesja_element}
        raise HTTPException(status_code=404, detail=f"Sesji {id} nie znaleziono")
    except bson.errors.InvalidId:
        raise HTTPException(status_code=404, detail=f"klucz id musi mieć 12 znaków")


@router.put("/zakoncz_sesje/id={id}", response_description="Zwróć jedną sesję")
async def zakoncz_sesje(id: str):
    try:
        sesja_find = db_miernik.zbior_sesji.find_one({"_id": ObjectId(id)})
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
            db_miernik.zbior_sesji.update_one({"_id": ObjectId(id)},
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

@router.delete("/delete_sesje/id_sesji={id}", response_description="Usuń sesje")
async def delete_sesja(id: str):
    delete_result = db_miernik.zbior_sesji.delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=403, detail=f"Sesje {id} nie znaleziono")


@router.delete("/drop_zbior_sesji/", response_description="drop sesje")  # , response_model=Wektor_Probek)
async def drop_sesje():
    db_miernik.zbior_sesji.drop()
    return HTTPException(status_code=404, detail=f"Kolekcje sesji nie możesz wyczyścić")
