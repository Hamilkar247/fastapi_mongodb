import random
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr
from pymongo import MongoClient
from bson import ObjectId
from typing import Optional, List

from models_miernik import PydanticObjectId


def get_paczka_danych_content():
    myrecord = {
        "czas_przyjscia_paczki": str(datetime.now()),
        "kod_status": "000000",
        "numer_seryjny_urzadzenia": "AXZC78744",
        "wartosci_pomiaru_sensorow": [
            {
                "litera_porzadkowa": "a",
                "wartosc": random.Random.randint(0, 9)
            },
            {
                "litera_porzadkowa": "b",
                "wartosc": random.Random.randint(0, 9)
            },
            {
                "litera_porzadkowa": "c",
                "wartosc": random.Random.randint(0, 9)
            }
        ]
    }
    return myrecord


class PaczkaDanychModel(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    czas_przyjscia_paczki: Optional[str]
    #wartosci: str #encja - wartosci pomiaru
    kod_statusu: str
    numer_seryjny_urzadzenia: str #sn

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
