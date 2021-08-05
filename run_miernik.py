from fastapi import FastAPI

import generateData
from models_miernik import User, db_testowo_miernik, dblist

app = FastAPI()


@app.post('/user/')
async def create_user(user: User):
    if hasattr(user, 'id'):
        delattr(user, 'id')
    ret = db_testowo_miernik.users.insert_one(user.dict(by_alias=True))
    user.id = ret.inserted_id
    return {'user': user}


@app.get('/user/')
async def get_users():
    users = []
    for user in db_testowo_miernik.users.find():
        users.append(User(**user))
    return {'users': users}
