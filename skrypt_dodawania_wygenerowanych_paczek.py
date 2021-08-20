
from bson import ObjectId

from models import db_miernik
from db_models.kolekcja_sesji_model import PaczkaDanychModel
from fastapi import Body


def dodawanie_do_aktywnej_sesji_nowych_paczek(paczka: PaczkaDanychModel):# = Body(...)):
    zbior_dokumentow_sesji = db_miernik.zbior_dokumentow_sesji
    liczba_aktywnych_sesji = zbior_dokumentow_sesji.find({"czy_aktywna": "tak"})
    print(liczba_aktywnych_sesji.count)
    if liczba_aktywnych_sesji.count() == 1:
        sesja_aktywna_find = zbior_dokumentow_sesji.find_one({"czy_aktywna": "tak"})
        print(sesja_aktywna_find)
        print(sesja_aktywna_find["czy_aktywna"])
        start_sesji=sesja_aktywna_find["start_sesji"]
        print(start_sesji)
        id_sesji = sesja_aktywna_find["_id"]
        print(id_sesji)
        if hasattr(paczka, 'id'):
            delattr(paczka, "id")
        paczka.czas_przyjscia_paczki = "xfa"
        paczka.kod_statusu = "casda"
        paczka.numer_seryjny_urzadzenia = "ahjo"
        zbior_dokumentow_sesji.update(
            { "_id": ObjectId(id_sesji)},
            {
              "$push":
                {
                "lista_paczek_danych":
                     {
                         "_id": paczka.id,
                         "czas_przyjscia_paczki": paczka.czas_przyjscia_paczki,
                         "kod_status": paczka.kod_statusu,
                         "numer_seryjny_urzadzenia": paczka.numer_seryjny_urzadzenia
                         #"PackSizeName":"xyz",
                         #"UnitName":"Polska"
                     }
                }
            }
        )

