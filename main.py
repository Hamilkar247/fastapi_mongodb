from fastapi import Depends, FastAPI

from dependencies import get_query_token, get_token_header
from internal import admin
from routers import items, users
from api_web import sesje, uzytkownicy, urzadzenia, sensory, paczki_danych, wartosci_pomiarow_sensorow, kolekcja_sesji

app = FastAPI()#dependencies=[Depends(get_query_token)])

#app.include_router(sesje.router)
#app.include_router(urzadzenia.router)
#app.include_router(sensory.router)
app.include_router(paczki_danych.router)
#app.include_router(wartosci_pomiarow_sensorow.router)
#app.include_router(uzytkownicy.router)
#app.include_router(users.router)
#app.include_router(items.router)
app.include_router(kolekcja_sesji.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    #dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

#from routers import items
#
#items.myfunc()