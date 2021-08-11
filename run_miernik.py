from fastapi import FastAPI, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.typing import List
from starlette import status
from starlette.responses import JSONResponse

import generateData
from models_miernik import UzytkownikModel, db_miernik, StudentModel, \
    UpdateStudentModel, Wektor_ProbekModel, UrzadzenieModel, SensorModel
from models_miernik import SesjaModel
from bson import ObjectId
from datetime import datetime


app = FastAPI()


@app.post("/sensor/", response_description="Stworz sensor", response_model=SensorModel)
async def create_sensor(sensor: SensorModel = Body(...)):
    if hasattr(sensor, "id"):
        delattr(sensor, "id")
    db_miernik.sensory.insert_one(sensor.dict(by_alias=True))
    sensory = jsonable_encoder(sensor)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=sensory)


@app.post("/sensor/{id}", response_description="Stwórz sensor, podlaczajac go pod urzadzenie", response_model=SensorModel)
async def create_sensor(id_urzadzenia: str, sensor: SensorModel = Body(...)):
    print(f"id_urzadzenia {id_urzadzenia}")
    urzadzenia = db_miernik.urzadzenia.find_one({"_id": ObjectId(id_urzadzenia)})
    print(urzadzenia)
    if urzadzenia is not None:
        if hasattr(sensor, "id"):
            delattr(sensor, "id")
        sensor.urzadzenie_id=id_urzadzenia
        db_miernik.sensory.insert_one(sensor.dict(by_alias=True))
        sensor = jsonable_encoder(sensor)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=sensor)
    else:
        raise HTTPException(status_code=404, detail=f"urządzenie o id:{id_urzadzenia} nie znaleziono!")


@app.get("/sensor/", response_description="Zwróć wszystkie sensory")
async def get_sensor():
    sensory_zbior = []
    for sensor in db_miernik.sensory.find():
        sensory_zbior.append(SensorModel(**sensor))
    return {"sensory": sensory_zbior}


@app.get("/sensor/{id}", response_description="Zwróć wszystkie sensory")
async def get_sensor_id(id: str):
    print(db_miernik["sensory"])
    if(sensory := db_miernik["sensory"].find_one({"_id": id})) is not None:
        return sensory
    raise HTTPException(status_code=404, detail=f"Sensory {id} nie znaleziono")


@app.delete("/delete_sensor/{id}", response_description="Usuń sensor")
async def delete_sensor(id: str):
    delete_result = db_miernik["sensory"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=403, detail=f"Sensora {id} nie znaleziono")


@app.delete("/drop_sensor/", response_description="drop sensory")
async def drop_sensor():
    db_miernik['sensory'].drop()
    return HTTPException(status_code=404, detail=f"Kolekcji sensory nie można wyczyścić")


@app.post("/urzadzenie/", response_description="Stwórz urządzenia", response_model=UrzadzenieModel)
async def create_urzadzenia(urzadzenie: UrzadzenieModel = Body(...)):
    if hasattr(urzadzenie, "id"):
        delattr(urzadzenie, "id")
    db_miernik.urzadzenia.insert_one(urzadzenie.dict(by_alias=True))
    urzadzenie = jsonable_encoder(urzadzenie)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=urzadzenie)


@app.post("/urzadzenie/{id_uzytkownik", response_description="Stwórz urządzenia", response_model=UrzadzenieModel)
async def create_urzadzenia(id_uzytkownika: str, urzadzenie: UrzadzenieModel = Body(...)):
    print(f"id_uzytkownika {id_uzytkownika}")
    uzytkownik = db_miernik.uzytkownicy.find_one({"_id": ObjectId(id_uzytkownika)})
    print(uzytkownik)
    if uzytkownik is not None:
        if hasattr(urzadzenie, "id"):
            delattr(urzadzenie, "id")
        urzadzenie.id_uzytkownika = id_uzytkownika
        db_miernik.urzadzenia.insert_one(urzadzenie.dict(by_alias=True))
        urzadzenie = jsonable_encoder(urzadzenie)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=urzadzenie)
    else:
        raise HTTPException(status_code=404, detail=f"Użytkownik o id: {id_uzytkownika} nie znaleziono")


@app.get('/urzadzenie/', response_description="Zwróc wszystkie urzadzenia")
async def get_urzadzenie():
    urzadzenia_zbior = []
    for urzadzenie in db_miernik.urzadzenia.find():
        urzadzenia_zbior.append(UrzadzenieModel(**urzadzenie))
    return {"urzadzenia": urzadzenia_zbior}


@app.get("/urzadzenie/{id}", response_description="Zwroc jedno urzadzenie")
async def get_urzadzenie_id(id: str):
    if (urzadzenia := db_miernik["urzadzenia"].find_one({"_id": id})) is not None:
        return urzadzenia
    raise HTTPException(status_code=404, detail=f"Urządzenia o id: {id} nie znaleziono")


@app.delete("/delete_urzadzenie/{id}", response_description="Usuń urzadzenie")
async def delete_urzadzenie(id: str):
    delete_result = db_miernik["urzadzenia"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=403, detail=f"Urzadzenie {id} nie znaleziono")


@app.delete("/drop_urzadzenie/", response_description="drop urzadzenia")
async def drop_urzadzenia():
    db_miernik['urzadzenia'].drop()
    return HTTPException(status_code=404, detail=f"Kolekcji urzadzeń nie można wyczyścić")


@app.post("/sesja/", response_description="Stworz sesje", response_model=SesjaModel)
async def create_sesja(sesja: SesjaModel = Body(...)):
    now = datetime.now()
    print("now =", now)
    dt_string = now.strftime("%d/%m/%y %H:%M:%S")
    print(f"date and time = {dt_string}")
    print(f"rozpoczecia : {sesja}")

    if hasattr(sesja, 'id'):
       delattr(sesja, 'id')
    sesja.start_sesji = dt_string
    sesja.koniec_sesji = "nie zakonczona"
    print(f"{sesja}")
    #wrzucamy do bazy danych wraz z wygenerowanym kluczem
    db_miernik.sesje.insert_one(sesja.dict(by_alias=True))
    sesja = jsonable_encoder(sesja)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=sesja)


@app.post("/sesja/{id_uzytkownika}", response_description="Stworz sesje", response_model=SesjaModel)
async def create_sesja(id_uzytkownika: str, sesja: SesjaModel = Body(...)):
    print(f"id_usera {id_uzytkownika}")
    now = datetime.now()
    print("now =", now)
    dt_string = now.strftime("%d/%m/%y %H:%M:%S")
    print(f"date and time = {dt_string}")
    print(f"rozpoczecia : {sesja}")

    print(f"id_uzytkownika: {id_uzytkownika}")
    uzytkownik = db_miernik.uzytkownicy.find_one({"_id": ObjectId(id_uzytkownika)})
    print(uzytkownik)
    if uzytkownik is not None:
        if hasattr(sesja, 'id'):
            delattr(sesja, 'id')
        sesja.id_uzytkownika=id_uzytkownika
        sesja.start_sesji = dt_string
        sesja.koniec_sesji = "nie zakonczona"
        print(f"{sesja}")
        #wrzucamy do bazy danych wraz z wygenerowanym kluczem
        db_miernik.sesje.insert_one(sesja.dict(by_alias=True))
        sesja = jsonable_encoder(sesja)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=sesja)
    else:
        raise HTTPException(status_code=404, detail=f"Użytkownika o id: {id_uzytkownika} nie znaleziono!")


@app.get('/sesja/', response_description="Zwroc wszystkie sesje")
async def get_sesje():
    sesje_zbior = []
    for sesja in db_miernik.sesje.find():
        sesje_zbior.append(SesjaModel(**sesja))
    return {"sesje": sesje_zbior}


@app.get("/sesja/{id}", response_description="Zwroc jedna sesje")
async def get_sesje_id(id: str):
    if (sesja := db_miernik['sesje'].find_one({"_id": id})) is not None:
        return sesja
    raise HTTPException(status_code=404, detail=f"Sesji {id} nie znaleziono")


@app.delete("/delete_sesja/{id}", response_description="Usuń sesje")
async def delete_sesja(id: str):
    delete_result = db_miernik["sesje"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=403, detail=f"Sesje {id} nie znaleziono")


@app.delete("/drop_sesje/", response_description="drop sesje")#, response_model=Wektor_Probek)
async def drop_sesje():
    db_miernik['sesje'].drop()
    return HTTPException(status_code=404, detail=f"Kolekcje sesji nie możesz wyczyścić")


@app.post("/wektor_probek/", response_description="Stworz wektor probek", response_model=Wektor_ProbekModel)
async def create_wektor_probek(wektor_probek: Wektor_ProbekModel = Body(...)):
    if hasattr(wektor_probek, 'id'):
        delattr(wektor_probek, 'id')
    db_miernik.wektory_probek.insert_one(wektor_probek.dict(by_alias=True))
    wektor_probek = jsonable_encoder(wektor_probek)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=wektor_probek)


@app.post("/wektor_probek/{id_sesji}", response_description="Stworz wektor probek, powiazany z konkretną sesją"
                                                            , response_model=Wektor_ProbekModel)
async def create_wektor_probek(id_sesji: str, wektor_probek: Wektor_ProbekModel = Body(...)):
    print(f"id_sesji {id_sesji}")
    sesje = db_miernik.sesje.find_one({"_id": ObjectId(id_sesji)})
    print(sesje)
    if sesje is not None:
        if hasattr(wektor_probek, "id"):
            delattr(wektor_probek, "id")
        wektor_probek.id_sesji = id_sesji
        db_miernik.wektory_probek.insert_one(wektor_probek.dict(by_alias=True))
        wektor_probek = jsonable_encoder(wektor_probek)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=wektor_probek)
    else:
        raise HTTPException(status_code=404, detail=f"sesji o id:{id_sesji} nie znaleziono!")


@app.get('/wektor_probek/', response_description="Zwroc wszystkie wektory probek")
async def get_wektory_probek():
    wektory_probek = []
    for wektor_probek in db_miernik.wektory_probek.find():
        wektory_probek.append(Wektor_ProbekModel(**wektor_probek))
    return {'wektory_probek': wektory_probek}


@app.get("/wektor_probek/{id}", response_description="Zwroc jedna probke")#, response_model=Wektor_Probek)
async def get_wektor_probek_id(id: str):
    if (wektor_probek := db_miernik["wektory_probek"].find_one({"_id": id})) is not None: #usuwam await przez db_miernik
        return wektor_probek
    raise HTTPException(status_code=404, detail=f"Wektor probek {id} nie znaleziono")


@app.delete("/delete_wektor_probek/{id}", response_description="Usuń wektor probek")
async def delete_wektor_probek(id: str):
    delete_result = db_miernik["wektory_probek"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Wektora próbek {id} nie znaleziono")


@app.delete("/drop_wektory_probek/", response_description="drop wektor_probek")#, response_model=Wektor_Probek)
async def drop_wektory_probek():
    db_miernik['wektory_probek'].drop()
    return HTTPException(status_code=404, detail=f"Kolekcja wektorów próbek nie możesz wyczyścić")


@app.post('/uzytkownik/')
async def create_uzytkownik(uzytkownik: UzytkownikModel):
    if hasattr(uzytkownik, 'id'):
        delattr(uzytkownik, 'id')
    db_miernik.uzytkownicy.insert_one(uzytkownik.dict(by_alias=True))
    uzytkownik.id = ret.inserted_id
    return {'uzytkownik': uzytkownik}


@app.get('/uzytkownik/')
async def get_uzytkownik():
    uzytkownicy = []
    for uzytkownik in db_miernik.uzytkownicy.find():
        uzytkownicy.append(UzytkownikModel(**uzytkownik))
    return {'uzytkownicy': uzytkownicy}


@app.post("/create_student/", response_description="Add new student", response_model=StudentModel)
async def create_student(student: StudentModel = Body(...)):
    print(f"rozpoczecie {student}")
    #student.id=ObjectId()
    student = jsonable_encoder(student)
    # await przed prawa stroną rownania - wywoluje blad
    new_student = db_miernik["students"].insert_one(student) #await przed prawa stroną rownania - wywoluje blad
    # await przed prawa stroną rownania - wywoluje blad
    created_student = db_miernik["students"].find_one({"_id": new_student.inserted_id})
    #id_student=ObjectId()
    print(created_student)
    #print(id_student)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)


@app.get("/list_students/", response_description="List all students") #, response_model=List[StudentModel])
async def list_students():
    students = []
    for student in db_miernik.students.find():
        #print(student)
        students.append(StudentModel(**student))
    return {'students': students}


@app.get("/show_students/{id}", response_description="Get a single student", response_model=StudentModel)
async def show_student(id: str):
    if (student := db_miernik["students"].find_one({"_id": id})) is not None: # usunalem await
        return student
    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.put("/update_student/{id}", response_description="Update a student")#, response_model=StudentModel)
async def update_student(id: str, student: UpdateStudentModel = Body(...)):
    student = {k: v for k, v in student.dict().items() if v is not None}
    if len(student) >= 1:
        update_result = db_miernik["students"].update_one({"_id": id}, {"$set": student})
        if update_result.modified_count == 1:
            if (
                update_student := db_miernik["students"].find_one({"_id": id})
            ) is not None:
                return update_student
    if (existing_student := db_miernik["students"].find_one({"_id": id})) is not None:
        return existing_student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.delete("/delete_student/{id}", response_description="Delete a student")
async def delete_student(id: str):
    delete_result = db_miernik["students"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.delete("/drop_students/", response_description="drop all students")
async def drop_student():
    db_miernik['students'].drop()
    return HTTPException(status_code=404, detail=f"Students collection cannot be droped")
