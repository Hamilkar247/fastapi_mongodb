from typing import List

from fastapi import FastAPI, status
from pydantic import BaseModel
from pymongo import MongoClient


DB = "slack"
MSG_COLLECTION = "messages"
USER_COLLECTION = "users"

DB = "slack"

# Message class defined in Pydantic
class Message(BaseModel):
    channel: str
    author: str
    text: str


class User(BaseModel):
    nickname: str


# Instantiate the FastAPI
app = FastAPI()


@app.get("/status")
def get_status():
    """Get status of messaging server."""
    return {"status": "running"}


@app.get("/users")
def get_users(nickname: str):
    """Get all users in list"""
    with MongoClient() as client:
        users_collection = client[DB][MSG_COLLECTION]
        user_list = users_collection.find({"nickname": nickname})
        response_user_list = []
        for user in user_list:
            response_user_list.append(User(**user))
        return response_user_list


@app.get("/channels", response_model=List[str])
def get_channels():
    """Get all channels in list from"""
    with MongoClient() as client:
        msg_collection = client[DB][MSG_COLLECTION]
        distinct_channel_list = msg_collection.distinct("channel")
        return distinct_channel_list


@app.get("/messages/{channel}", response_model=List[Message])
def get_messages(channel: str):
    """Get all messages for the specified channel"""
    with MongoClient() as client:
        msg_collection = client[DB][MSG_COLLECTION]
        msg_list = msg_collection.find({"channel": channel})
        response_msg_list = []
        for msg in msg_list:
            response_msg_list.append(Message(**msg))
        return response_msg_list


@app.post("/post_message", status_code=status.HTTP_201_CREATED)
def post_message(message: Message):
    """Post a new message to the specified channel."""
    with MongoClient() as client:
        msg_collection = client[DB][MSG_COLLECTION]
        result = msg_collection.insert_one(message.dict())
        ack = result.acknowledged
        return {"insertion": ack}


@app.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    with MongoClient() as client:
        user_collection = client[DB][USER_COLLECTION]
        result = user_collection.insert_one(user.dict())
        ack = result.acknowledged
        return {"insertion": ack}



#import pprint
#
##inspiracja
## https://medium.com/fastapi-tutorials/integrating-fastapi-and-mongodb-8ef4f2ca68ad
#
#client = MongoClient()
#
#db = client["slack"]
#msg_collection = db["messages"]
#
#
##Create a message dict
#message = {
#    "channel": "dev",
#    "author": "cerami",
#    "text": "Hello, world!"
#}
#
#result = msg_collection.insert_one(message)
#print(result.inserted_id)
#
#pp = pprint.PrettyPrinter(indent=4)
#for doc in msg_collection.find():
#    pp.pprint(doc)
#
#record_list = msg_collection.find(({"channel": "dev"}))
#
#record_list = msg_collection.find({"author": "cerami"})