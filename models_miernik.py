from pydantic import BaseModel, Field, EmailStr
from pymongo import MongoClient
from bson import ObjectId
from typing import Optional

client = MongoClient("mongodb://localhost:27017")
db_miernik = client["miernik"]
print(client.list_database_names())
print(db_miernik.list_collection_names())
print(f"ahoj! {db_miernik['zbior_dokumentow_sesji']}")
#if "sesje" in db_miernik:
#    print("baza danych już istnieje")
#    print(db_miernik['sesje'])

record = {
  "nazwa_sesji": "str",
  "start_sesji": "17/08/21 15:12:22",
  "koniec_sesji": "nie zakonczona",
  "czy_aktywna": "true",
  "dlugosc_trwania_w_s": "trwa - dlugosc nieustalona",
  "id_urzadzenia": "str",
  "id_uzytkownika": "str",
  "paczki_danych": "str"
}

mycol = db_miernik["zbior_dokumentow_sesji"]
x = mycol.insert_one(record)
print(x)

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


class UzytkownikModel(BaseModel):
    # uwaga - pydantic nie obsluguje nazw _id, z kolei mongodb tak zaczyna idki-stąd alias
    id: Optional[PydanticObjectId] = Field(alias='_id')
    nick: str
    email: str
    dane_osobowe: str
    stanowisko: str
    opis: str
    uprawnienia: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class PaczkaDanychModel(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    czas_paczki: Optional[str]
    #wartosci: str #encja - wartosci pomiaru
    kod_statusu: str
    numer_seryjny: str
    id_urzadzenia: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "numer_seryjny": "str",
                "kod_statusu": "00000000"
            }
        }


class WartoscPomiaruSensora(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    wartosc: str
    litera: str
    id_paczki_danych: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbritrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "wartosc": 3,
                "litera": "str"
            }
        }


class SesjaModel(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    nazwa_sesji: str
    start_sesji: Optional[str]
    koniec_sesji: Optional[str]
    czy_aktywna: Optional[str]  #czy dopisujemy do paczel
    dlugosc_trwania_w_s: Optional[str]
    id_urzadzenia: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "nazwa_sesji": "str",
            }
        }


class UrzadzeniaModel(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    nazwa_urzadzenia: str
    numer_seryjny: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "nazwa_urzadzenia": "str",
                "numer_seryjny": "str",
            }
        }


class SensorModel(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    litera_porzadkowa: str
    parametr: str
    kalib_wspol: str
    min: str
    max: str
    jednostka: str
    status_sensora: str
    id_urzadzenia: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "litera_porzadkowa": "str",
                "parametr": "str",
                "kalib_wspol": "1;0",
                "min": "0",
                "max": "10",
                "jednostka": "str",
                "status_sensora": "aktywny"
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
