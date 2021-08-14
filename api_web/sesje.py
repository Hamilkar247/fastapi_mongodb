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


@router.post("/{id_urzadzenie}", response_description="Stworz sesje", response_model=SesjaModel)
async def create_sesja(id_urzadzenie: str, sesja: SesjaModel = Body(...)):
    now = datetime.now()
    print("now =", now)
    dt_string = now.strftime("%d/%m/%y %H:%M:%S")
    print(f"date and time = {dt_string}")
    print(f"rozpoczecia : {sesja}")
    print(f"id_urzadzenie: "+id_urzadzenie)

    urzadzenie_result = db_miernik.urzadzenia.find_one(id_urzadzenie)
    if urzadzenie_result is None:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    else:
        if hasattr(sesja, 'id'):
           delattr(sesja, 'id')
        sesja.id_urzadzenia = ObjectId(id_urzadzenie)
        sesja.czy_aktywna = "true"
        sesja.dlugosc_trwania = "trwa - dlugosc nieustalona"
        sesja.start_sesji = dt_string
        sesja.koniec_sesji = "nie zakonczona"
        print(f"{sesja}")
        #wrzucamy do bazy danych wraz z wygenerowanym kluczem
        db_miernik.sesje.insert_one(sesja.dict(by_alias=True))
        sesja = jsonable_encoder(sesja)
    else:
        print("Nie znaleziono urzadzenia w zbiorze")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Nie znaleziono urządzenia o tym id")
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=sesja)


@router.get('/', response_description="Zwroc wszystkie sesje")
async def get_sesje():
    sesje_zbior = []
    for sesja in db_miernik.sesje.find():
        sesje_zbior.append(SesjaModel(**sesja))
    return {"sesje": sesje_zbior}


@router.get("/{id}", response_description="Zwroc jedna sesje")
async def get_id_sesje(id: str):
    if (sesja := db_miernik['sesje'].find_one({"_id": id})) is not None:
        return sesja
    raise HTTPException(status_code=404, detail=f"Sesji {id} nie znaleziono")


@router.delete("/delete/{id}", response_description="Usuń sesje")
async def delete_sesja(id: str):
    delete_result = db_miernik["sesje"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=403, detail=f"Sesje {id} nie znaleziono")


@router.delete("/drop_sesje/", response_description="drop sesje")#, response_model=Wektor_Probek)
async def drop_sesje():
    db_miernik['sesje'].drop()
    return HTTPException(status_code=404, detail=f"Kolekcje sesji nie możesz wyczyścić")
