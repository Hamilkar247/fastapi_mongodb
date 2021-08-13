from fastapi import FastAPI, Body, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse
from models_miernik import db_miernik, SensorModel

router = APIRouter(
    prefix="/sensory",
    tags=["sensory"],
    responses={404: {"description": "Not"}}
)


@router.post("/", response_description="Stworz sensory", response_model=SensorModel)
async def create_sensor(sensor: SensorModel = Body(...)):
    print(f"rozpoczecie {sensor}")
    if hasattr(sensor, 'id'):
        delattr(sensor, 'id')
    ret = db_miernik.sensor.insert_one(sensor.dict(by_alias=True))
    sensor.id = ret.inserted_id
    print(f"rozpoczecie {sensor}")
    sensor = jsonable_encoder(sensor)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=sensor)


@router.get('/', response_description="Zwroc wszystkie sensor")
async def get_sensor():
    sensory = []
    for sensor in db_miernik.sensor.find():
        sensory.append(SensorModel(**sensory))
    return {'sensory': sensory}


@router.get("/{id}", response_description="Zwroc jeden sensor")#, response_model=Wektor_Probek)
async def get_sensor_po_id(id: str):
    if (sensor := db_miernik["sensory"].find_one({"_id": id})) is not None: #usuwam await przez db_miernik
        return sensor
    raise HTTPException(status_code=404, detail=f"Sensor o {id} nie znaleziono")


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

