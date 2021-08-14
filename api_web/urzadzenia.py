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


@router.post("/", response_description="Stworz urzadzenia", response_model=UrzadzeniaModel)
async def create_urzadzenia(urzadzenie: UrzadzeniaModel = Body(...)):
    print(f"rozpoczecie {urzadzenie}")
    if hasattr(urzadzenie, "id"):
        delattr(urzadzenie, "id")
    ret = db_miernik.zbior_urzadzen.insert_one(urzadzenie.dict(by_alias=True))
    urzadzenie.id = ret.inserted_id
    print(f"rozpoczecie {urzadzenie}")
    urzadzenie = jsonable_encoder(urzadzenie)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=urzadzenie)


@router.get('/', response_description="Zwróć wszystkie urządzenia")
async def get_urzadzenia():
    urzadzenia_zbior = []
    for urzadzenie in db_miernik.zbior_urzadzen.find():
        urzadzenia_zbior.append(UrzadzeniaModel(**urzadzenie))
    return {"urzadzenia": urzadzenia_zbior}


@router.get("/{id}", response_description="Zwroc jedna paczke danych")
async def get_urzadzenie(id: str):
    if (urzadzenia := db_miernik.zbior_urzadzen.find_one({"_id": id})) is not None:
        return urzadzenia
    raise HTTPException(status_code=404, detail=f"Paczki danych o {id} nie znaleziono")


@router.delete("/delete/{id}", response_description="Usuń paczki danych")
async def delete_urzadzenia(id: str):
    delete_result = db_miernik.zbior_urzadzen.delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    elif delete_result.deleted_count > 1:
        return HTTPException(status_code=403, detail=f"jest wiecej niz jeden wynik!")
    raise HTTPException(status_code=403, detail=f"Urządzenie o id:{id} nie znaleziono!")


@router.delete("/drop_urzadzenia", response_description="drop urzadzenia")
async def drop_urzadzenia():
    db_miernik.zbior_urzadzen.drop()
    #tu wypadaloby dać jakiś return - nie mam pomyslu jaki
    raise HTTPException(status_code=404, detail=f"Kolekcja wektorów próbek nie możesz wyczyścić")
