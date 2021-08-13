from pydantic import BaseModel, Field, EmailStr
from pydantic.decorator import List
from pymongo import MongoClient
from bson import ObjectId
from typing import Optional

client = MongoClient("mongodb://localhost:27017")
db_miernik = client["miernik"]
print(client.list_database_names())
print(db_miernik.list_collection_names())
print(db_miernik["sesje"])
#if "sesje" in db_miernik:
#    print("baza danych już istnieje")
#    print(db_miernik['sesje'])
mycol = db_miernik["sesje"]
for x in mycol.find():
    print(x)


class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class SesjaModel(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    nazwa_sesji: str
    start_sesji: Optional[str]
    koniec_sesji: Optional[str]
    owner: Optional[str]
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "nazwa_sesji": "str"
            }
        }


class UzytkownikModel(BaseModel):
    # uwaga - pydantic nie obsluguje nazw _id, z kolei mongodb tak zaczyna idki-stąd alias
    id: Optional[PydanticObjectId] = Field(alias='_id')
    imie: str
    nick: str
    email: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            "example": {
                "imie": "str",
                "nick": "str",
                "email": "str"
            }
        }


class Wektor_ProbekModel(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    chlorowodor: Optional[str]
    fluorowodor: Optional[str]
    formaldechyd: Optional[str]
    pm1: Optional[str]
    pm2_5: Optional[str]
    pm5: Optional[str]
    id_sesji: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "chlorowodor": "0.06",
                "fluorowodor": "2.4",
                "formaldechyd": "2.0",
                "pm1": "3.2",
                "pm2_5": "2.4",
                "pm5": "1"
            }
        }


class PomiarModel(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    sensor_id: Optional[str]
    badany_parametr: Optional[str]
    zarejestrowana_wartosc: Optional[str]
    czas_zarejestrowania_pomiaru: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
            }
        }


class UrzadzenieModel(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    nazwa_urzadzenia: str
    id_uzytkownika: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "nazwa_urzadzenia": "str"
            }
        }


class SensorModel(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    nazwa_sensora: str
    badany_parametr: str
    urzadzenie_id: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "nazwa_sensora": "str",
                "badany_parametr": "str"
            }
        }


class StudentModel(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    name: str #= Field(...)
    email: EmailStr #= Field(...)
    course: str #= Field(...)
    gpa: float #= Field(..., le=4.0)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                #                "_id": "610d2eb8065fa7030e307ab3",
                "_id": "610d2eb8065fa7030e307ab3",
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": "3.0",
            }
        }


class UpdateStudentModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    course: Optional[str]
    gpa: Optional[float]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": "3.0",
            }
        }
