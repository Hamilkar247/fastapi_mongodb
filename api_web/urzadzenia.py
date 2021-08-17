from bson import ObjectId
from fastapi import FastAPI, Body, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse
from models_miernik import db_miernik, UrzadzeniaModel

router = APIRouter(
    prefix="/urzadzenia",
    tags=["urzadzenia"],
    responses={404: {"description": "Not"}}
)


@router.post("/stworz_urzadzenie", response_description="Stworz urzadzenia", response_model=UrzadzeniaModel)
async def create_urzadzenia(urzadzenie: UrzadzeniaModel = Body(...)):
    print(f"rozpoczecie {urzadzenie}")
    if hasattr(urzadzenie, "id"):
        delattr(urzadzenie, "id")
    ret = db_miernik.zbior_urzadzen.insert_one(urzadzenie.dict(by_alias=True))
    urzadzenie.id = ret.inserted_id
    print(f"rozpoczecie {urzadzenie}")
    urzadzenie = jsonable_encoder(urzadzenie)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=urzadzenie)


@router.get('/get_zbior_urzadzen', response_description="Zwróć wszystkie urządzenia")
async def get_zbior_urzadzen():
    urzadzenia_zbior = []
    for urzadzenie in db_miernik.zbior_urzadzen.find():
        urzadzenia_zbior.append(UrzadzeniaModel(**urzadzenie))
    return {"urzadzenia": urzadzenia_zbior}


@router.get("/get_urzadzenie/id={id}", response_description="Zwroc jedno urzadzenie")
async def get_urzadzenie_id(id: str):
    urzadzenie = db_miernik.zbior_urzadzen.find_one({"_id": ObjectId(id)})
    if urzadzenie is not None:
        print(urzadzenie)
        urzadzenie_element = []
        urzadzenie_element.append(UrzadzeniaModel(**urzadzenie))
        return {"urzadzenie_element": urzadzenie_element}
    raise HTTPException(status_code=404, detail=f"Urządzenia o {id} nie znaleziono")


@router.delete("/delete_urzadzenie/id_urzadzenia={id}", response_description="Usuń paczki danych")
async def delete_urzadzenia(id: str):
    delete_result = db_miernik.zbior_urzadzen.delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    elif delete_result.deleted_count > 1:
        return HTTPException(status_code=403, detail=f"jest wiecej niz jeden wynik!")
    raise HTTPException(status_code=403, detail=f"Urządzenie o id:{id} nie znaleziono!")


@router.delete("/drop_zbior_urzadzen", response_description="drop urzadzenia")
async def drop_urzadzenia():
    db_miernik.zbior_urzadzen.drop()
    #tu wypadaloby dać jakiś return - nie mam pomyslu jaki
    raise HTTPException(status_code=404, detail=f"Kolekcja wektorów próbek nie możesz wyczyścić")
