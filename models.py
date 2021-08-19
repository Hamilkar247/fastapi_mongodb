from pydantic import BaseModel, Field
from pymongo import MongoClient
from bson import ObjectId
from typing import Optional

#client = MongoClient()
#db = client.test
#print(client.list_database_names())
#dblist = client.list_database_names()
#if "api_miernik_reczny" in dblist:
#    print("The database exists.")

#col = db["blog_posts"]
#print(db.list_collection_names())
#print(col.drop())
#print(db.list_collection_names())
import generateData
from mongo_models import wektor_danych

client = MongoClient("mongodb://localhost:27017")
db_miernik = client["api_miernik"]
#print(client.list_database_names())
#dblist = client.list_database_names()
#if "api_miernik" in dblist:
#    print("baza danych już istnieje")
#wektor_probek_col = db_miernik["wektory_probek"]
#wektor_probek = [generateData.generataVector()]
#dane_probkowe = {
#     "temperatura": wektor_probek.__getitem__(0)[0],
#     "pm2_5": wektor_probek.__getitem__(0)[1],
#     "pm5": wektor_probek.__getitem__(0)[2],
#     "pm10": wektor_probek.__getitem__(0)[3],
#     "hydroetyl": wektor_probek.__getitem__(0)[4],
#     "tlen": wektor_probek.__getitem__(0)[5]
#}


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


class Wektor_Probek:
    _id: Optional[PydanticObjectId] = Field(alias="_id")
    temperatura: str
    pm2_5: str
    pm5: str
    pm10: str
    hydroetyl: str
    tlen: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class Pomiar:
    lista_probek=[]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class Sesja:
    _id: Optional[PydanticObjectId] = Field(alias="_id")
    start_sesji: str
    koniec_sesji: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class User(BaseModel):
    _id: Optional[PydanticObjectId] = Field(alias='_id')
    name: str
    username: str
    email: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class Blog_post(BaseModel):
    _id: Optional[PydanticObjectId] = Field(alias='_id')
    title: str
    author: str
    content: str #Text
    #created_at: datetime = datetime.now()
    #published_at: datetime
    #published: Optional[bool] = False

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

