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

client = MongoClient("mongodb://localhost:27017")
db_miernik = client["api_miernik"]
print(client.list_database_names())
dblist = client.list_database_names()
if "api_miernik" in dblist:
    print("The database exist")


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


class Probka:
    temperatura: int
    pm2_5: int
    pm5: int
    pm10: int
    hydroetyl: int
    tlen: int

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
    start_sesji: bool
    koniec_sesji: bool

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

