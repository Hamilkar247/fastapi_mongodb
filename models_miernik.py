from pydantic import BaseModel, Field, EmailStr
from pymongo import MongoClient
from bson import ObjectId
from typing import Optional

client = MongoClient("mongodb://localhost:27017")
db_miernik = client["miernik"]
print(client.list_database_names())
dblist = client.list_database_names()
if "miernik" in dblist:
    print("baza danych już istnieje")

# user = db_testowo_miernik["user"]


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


class UserModel(BaseModel):
    # uwaga - pydantic nie obsluguje nazw _id, z kolei mongodb tak zaczyna idki-stąd alias
    id: Optional[PydanticObjectId] = Field(alias='_id')
    name: str
    username: str
    email: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class Wektor_ProbekModel(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    temperatura: str
    pm2_5: str
    pm5: str
    pm10: str
    hydroetyl: str
    tlen: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "610d2eb8065fa7030e307ab3",
                "temperatura": "10 C",
                "pm2_5": "2",
                "pm5": "1",
                "pm10": "3.2",
                "hydroetyl": "2.4",
                "tlen": "2.0"
            }
        }


class SesjaModel:
    _id: Optional[PydanticObjectId] = Field(alias="_id")
    start_sesji: str
    koniec_sesji: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
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
