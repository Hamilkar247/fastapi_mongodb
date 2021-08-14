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


@router.post("/", response_description="Stworz sensory", response_model=SensorModel)
async def create_sensor(sensor: SensorModel = Body(...)):
    print(f"rozpoczecie {sensor}")
    if hasattr(sensor, 'id'):
        delattr(sensor, 'id')
    ret = db_miernik.zbior_sensorow.insert_one(sensor.dict(by_alias=True))
    sensor.id = ret.inserted_id
    print(f"rozpoczecie {sensor}")
    sensor = jsonable_encoder(sensor)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=sensor)


@router.get('/', response_description="Zwroc wszystkie sensor")
async def get_sensor():
    sensory_zbior = []
    for sensor in db_miernik.zbior_sensorow.find():
        sensory_zbior.append(SensorModel(**sensory_zbior))
    return {'sensory': sensory_zbior}


@router.get("/{id}", response_description="Zwroc jeden sensor")#, response_model=Wektor_Probek)
async def get_sensor_id(id: str):
    sensor = db_miernik.zbior_sensor.find_one({"_id": ObjectId(id)})
    if sensor is not None:
        sensor_element = []
        sensor_element.append(SensorModel(**sensor))
        return {"sensor_element": sensor_element}
    raise HTTPException(status_code=404, detail=f"Sensor o {id} nie znaleziono")


@router.delete("/delete/{id}", response_description="Usuń sensor")
async def delete_sensor(id: str):
    ## DO DODANIA - do zastanowienia sie czy to powinno być usuniecie kaskadowa
    delete_result = db_miernik.zbior_sensorow.delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=403, detail=f"Sensora o {id} nie znaleziono")


@router.delete("/drop_paczki_danych/", response_description="drop sensor")#, response_model=Wektor_Probek)
async def drop_paczki_danych():
    db_miernik.zbior_sensorow.drop()
    return HTTPException(status_code=404, detail=f"Kolekcja wektorów próbek nie możesz wyczyścić")

