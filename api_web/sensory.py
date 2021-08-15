import bson
from bson import ObjectId
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


@router.post("/stworz_sesje/bez_id_urzadzenia", response_description="Stworz sensor", response_model=SensorModel)
async def create_sensor_bez_id_urzadzenia(sensor: SensorModel = Body(...)):
    if hasattr(sensor, 'id'):
        delattr(sensor, 'id')
    ret = db_miernik.zbior_sensorow.insert_one(sensor.dict(by_alias=True))
    sensor.id = ret.inserted_id
    print(f"sensor {sensor}")
    sensor = jsonable_encoder(sensor)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=sensor)


@router.post("/stworz_sesje/id_urzadzenia={id_urzadzenia}", response_description="Stwórz sensor", response_model=SensorModel)
async def create_sensor(id_urzadzenia: str, sensor: SensorModel = Body(...)):
    try:
        urzadzenie_result = db_miernik.zbior_urzadzen.find_one({"_id": ObjectId(id_urzadzenia)})
        if urzadzenie_result is None:
            print("Nie znaleziono urządzenia w zbiorze !")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Nie znaleziono urzadzenia o tym id")
        else:
            if hasattr(sensor, 'id'):
                delattr(sensor, 'id')
            sensor.id_urzadzenia = id_urzadzenia
            db_miernik.zbior_sensorow.insert_one(sensor.dict(by_alias=True))
            print(f"sensor {sensor}")
            sensor = jsonable_encoder(sensor)
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=sensor)
    except bson.errors.InvalidId:
        raise HTTPException(status_code=404, detail=f"klucz id musi mieć 12 znaków")


@router.get('/', response_description="Zwróć wszystkie sensory")
async def get_sensor():
    sensory_zbior = []
    for sensor in db_miernik.zbior_sensorow.find():
        sensory_zbior.append(SensorModel(**sensor))
    return {'sensory': sensory_zbior}


@router.get("/{id}", response_description="Zwroc jeden sensor")#, response_model=Wektor_Probek)
async def get_sensor_id(id: str):
    try:
        sensor = db_miernik.zbior_sensor.find_one({"_id": ObjectId(id)})
        if sensor is not None:
            sensor_element = []
            sensor_element.append(SensorModel(**sensor))
            return {"sensor_element": sensor_element}
        raise HTTPException(status_code=404, detail=f"Sensor o {id} nie znaleziono")
    except bson.errors.InvalidId:
        raise HTTPException(status_code=404, detail=f"klucz id musi mieć 12 znaków")


@router.delete("/delete/{id}", response_description="Usuń sensor")
async def delete_sensor(id: str):
    try:
        ## DO DODANIA - do zastanowienia sie czy to powinno być usuniecie kaskadowa
        delete_result = db_miernik.zbior_sensorow.delete_one({"_id": ObjectId(id)})
        if delete_result.deleted_count == 1:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        raise HTTPException(status_code=403, detail=f"Sensora o {id} nie znaleziono")
    except bson.errors.InvalidId:
        raise HTTPException(status_code=404, detail=f"klucz id musi mieć 12 znaków")


@router.delete("/drop_paczki_danych/", response_description="drop sensor")#, response_model=Wektor_Probek)
async def drop_paczki_danych():
    db_miernik.zbior_sensorow.drop()
    return HTTPException(status_code=404, detail=f"Kolekcja wektorów próbek nie możesz wyczyścić")

