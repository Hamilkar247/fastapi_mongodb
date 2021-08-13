from fastapi import FastAPI, Body, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse
from models_miernik import db_miernik, UrzadzeniaModel
from models_miernik import SesjaModel
from datetime import datetime


###### przyklad czasu
##datetime object containing current date and time
#now = datetime.now()
#print("now =", now)
## dd/mm/yy H:M:S
#dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#print("date and time =", dt_string)


router = APIRouter(
    prefix="/urzadzenia",
    tags=["urzadzenia"],
    responses={404: {"description": "Not"}}
)


@router.post("/", response_description="Stworz urzadzenia", response_model=UrzadzeniaModel)
async def create_urzadzenia(urzadzenie: UrzadzeniaModel = Body(...)):
    print(f"rozpoczecie {urzadzenie}")
    if hasattr(urzadzenie, "id"):
        delattr(urzadzenie, "id")
    ret = db_miernik.urzadzenia.insert_one(urzadzenie.dict)
    urzadzenie.id = ret.inserted_id
    print(f"rozpoczecie {urzadzenie}")
    urzadzenie = jsonable_encoder(urzadzenie)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=urzadzenie)


@router.get("/{id}", response_description="Zwroc jedna paczke danych")
async def get_urzadzenie(id: str):
    if (urzadzenia := db_miernik["urzedzenia"].find_one({"_id": id})) is not None:
        return urzadzenia
    raise HTTPException(status_code=404, detail=f"Paczki danych o {id} nie znaleziono")


@router.delete("/delete/{id}", response_description="Usuń paczki danych")
async def delete_urzadzenia(id: str):
    delete_result = db_miernik["urzedzenia"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    elif delete_result.deleted_count > 1:
        return HTTPException(status_code=403, detail=f"jest wiecej niz jeden wynik!")
    raise HTTPException(status_code=403, detail=f"Urządzenie o id:{id} nie znaleziono!")


@router.delete("/drop_urzadzenia", response_description="drop urzadzenia")
async def drop_urzadzenia():
    db_miernik["urzadzenia"].drop()
    #tu wypadaloby dać jakiś return - nie mam pomyslu jaki
    raise HTTPException(status_code=404, detail=f"Kolekcja wektorów próbek nie możesz wyczyścić")
