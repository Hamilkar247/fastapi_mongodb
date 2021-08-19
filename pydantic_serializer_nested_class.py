from pprint import pprint
from typing import Optional, List

from bson import ObjectId
from pydantic import BaseModel, Field

from models import PydanticObjectId, db_miernik


class PaczkaDanychModel(BaseModel):
    id: ObjectId#Optional[PydanticObjectId] = Field(alias="_id")
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
        json_encoders = {ObjectId: str}#,
                         #PaczkaDanychModel.__json_encoder__(): str}
        schema_extra = {
            "example": {
                "nazwa_sesji": "str",
            }
        }

ahjo=db_miernik.zbior_dokumentow_sesji.find_one({"_id": ObjectId("611cf4c00ba46a88aca581a6")})


#m_paczka = PaczkaDanychModel(id=ObjectId("507f191e810c19729de860ea"),
#                      czas_przyjscia_paczki="aaaa",
#                      kod_statusu="0000000",
#                      numer_seryjny_urzadzenia="10001010")
#

m_sesja = SesjaModel(id=ObjectId("611cf4c00ba46a88aca581a6"),
                     nazwa_sesji="o moj boze",
                     start_sesji="1231",
                     koniec_sesji="243243",
                     czy_aktywna="trwa",
                     dlugosc_trwania_w_s="132",
                     id_urzadzenia=None,
                     id_uzytkownika=None,
                     lista_paczek_danych=[])

#print("\npaczka danych - wyswietlenie")
#print(m_paczka.json())
#print("\nsesja - wyswietlenie")
#print(m_sesja.json())
#json=m_sesja.json()
#db_miernik.zbior_dokumentow_sesji.insert_one(m_sesja.json())

#ahjo = db_miernik.zbior_dokumentow_sesji.find_one({"_id": ObjectId("611cf4c00ba46a88aca581a6")})
#
#print("ahjo"+ahjo)
#ahjo = SesjaModel(**ahjo)
