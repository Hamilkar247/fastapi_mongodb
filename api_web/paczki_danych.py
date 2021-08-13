from fastapi import FastAPI, Body, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse
from models_miernik import  db_miernik, PaczkaDanychModel


###### przyklad czasu
##datetime object containing current date and time
#now = datetime.now()
#print("now =", now)
## dd/mm/yy H:M:S
#dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#print("date and time =", dt_string)


router = APIRouter(
    prefix="/paczki_danych",
    tags=["paczki_danych"],
    responses={404: {"description": "Not"}}
)


@router.post("/", response_description="Stworz paczke danych", response_model=PaczkaDanychModel)
async def create_paczke_danych(paczka_danych: PaczkaDanychModel = Body(...)):
    print(f"rozpoczecie {paczka_danych}")
    if hasattr(paczka_danych, 'id'):
        delattr(paczka_danych, 'id')
    ret = db_miernik.paczka_danych.insert_one(paczka_danych.dict(by_alias=True))
    paczka_danych.id = ret.inserted_id
    print(f"rozpoczecie {paczka_danych}")
    paczka_danych = jsonable_encoder(paczka_danych)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=paczka_danych)


    #wektor_probek = jsonable_encoder(wektor_probek)
    #new_wektor_probek = db_miernik["wektory_probek"].insert_one(wektor_probek)
    #created_student = db_miernik["wektory_probek"].find_one({"_id": new_wektor_probek.inserted_id})
    #print(created_student)
    #return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)

    #if hasattr(wektor_probek, 'id'):
    #    delattr(wektor_probek, 'id')
    #ret = db_miernik.wektory_probek.insert_one(wektor_probek.dict(by_alias=True))
    #wektor_probek.id = ret.inserted_id
    #return {'wektor_probek': wektor_probek}


@router.get('/', response_description="Zwroc wszystkie paczki danych")
async def get_paczki_danych():
    paczki_danych = []
    for paczka_danych in db_miernik.paczki_danych.find():
        paczka_danych.append(PaczkaDanychModel(**paczki_danych))
    return {'paczka_danych': paczka_danych}


@router.get("/{id}", response_description="Zwroc jedna paczke danych")#, response_model=Wektor_Probek)
async def pokaz_paczke_danych(id: str):
    mycol = db_miernik['paczki_danych']
    for x in db_miernik['paczki_danych'].find():
        print(x)

    if (paczki_danych := db_miernik["paczki_danych"].find_one({"_id": id})) is not None: #usuwam await przez db_miernik
        return paczki_danych
    raise HTTPException(status_code=404, detail=f"Paczki danych o {id} nie znaleziono")


@router.delete("/delete/{id}", response_description="Usuń paczki danych")
async def delete_paczki_danych(id: str):
    ## DO DODANIA - do zastanowienia sie czy to powinno być usuniecie kaskadowa
    delete_result = db_miernik["paczki_danych"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=403, detail=f"Paczki danych o {id} nie znaleziono")


@router.delete("/drop_paczki_danych/", response_description="drop paczki danych")#, response_model=Wektor_Probek)
async def drop_paczki_danych():
    db_miernik['paczki_danych'].drop()
    return HTTPException(status_code=404, detail=f"Kolekcja wektorów próbek nie możesz wyczyścić")

