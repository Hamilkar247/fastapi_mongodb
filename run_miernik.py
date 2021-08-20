from fastapi import FastAPI, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse
from models_miernik import UzytkownikModel, db_miernik, StudentModel, UpdateStudentModel, Wektor_ProbekModel
from models_miernik import SesjaModel
from datetime import datetime


###### przyklad czasu
##datetime object containing current date and time
#now = datetime.now()
#print("now =", now)
## dd/mm/yy H:M:S
#dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#print("date and time =", dt_string)


app = FastAPI()


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
