import random
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr
from pymongo import MongoClient
from bson import ObjectId
from typing import Optional, List


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


class PaczkaDanychModel(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    czas_przyjscia_paczki: Optional[str]
    #wartosci: str #encja - wartosci pomiaru
    kod_statusu: str
    numer_seryjny_urzadzenia: Optional[str] #sn

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


class SesjaModel(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    nazwa_sesji: str
    start_sesji: Optional[str]
    koniec_sesji: Optional[str]
    czy_aktywna: Optional[str]  # czy dopisujemy do paczel
    dlugosc_trwania_w_s: Optional[str]
    id_urzadzenia: Optional[str]
    id_uzytkownika: Optional[str]
    lista_paczek_danych: Optional[List[PaczkaDanychModel]] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "nazwa_sesji": "str",
            }
        }

