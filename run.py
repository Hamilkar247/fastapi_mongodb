from fastapi import FastAPI

import generateData
from models import db_miernik, dblist, User, Wektor_Probek  # , User, Blog_post, dblist

app = FastAPI()

sesja_dane = {
    "data": "10.10.2021",
    "start": "True",
    "koniec": "False"
}
sesja = db_miernik["sesja"]
#print(sesja.drop())
#sesje_lista = []
#x = sesja.insert_one(sesja_dane)
#print(x.inserted_id)
#y = {"": ""}
#for x in sesja.find():
#    print(x)
#    sesje_lista.append(x)


#wektor_probek = db_miernik["wektor_probek"]
#wektor_probek.drop()
#wektor_danych = []
#wektor_danych.append(generateData.generataVector())
#dane_pomiarowe = {
#    "temperatura": wektor_danych.__getitem__(0)[0],
#    "pm2_5": wektor_danych.__getitem__(0)[1],
#    "pm5": wektor_danych.__getitem__(0)[2],
#    "pm10": wektor_danych.__getitem__(0)[3],
#    "hydroetyl": wektor_danych.__getitem__(0)[4],
#    "tlen": wektor_danych.__getitem__(0)[5]
#}
#x = wektor_probek.insert_one(dane_pomiarowe)
#for x in wektor_probek.find():
#    print(x)


# probki = []
# if "api_miernik" in dblist:
#    print("The database exist")
# if True:
#    pomiar = db_miernik["pomiar"]
# wektor_danych = []
# wektor_danych.append(generateData.generataVector())
# dane_pomiarowe = {
#    "temperatura": wektor_danych.__getitem__(-1)[0],
#    "pm1_5": wektor_danych.__getitem__(0)[1],
#    "pm4": wektor_danych.__getitem__(0)[2],
#    "pm9": wektor_danych.__getitem__(0)[3],
#    "hydroetyl": wektor_danych.__getitem__(-1)[4],
#    "tlen": wektor_danych.__getitem__(-1)[5]
# }
# pomiar.insert_one(dane_pomiarowe)
# for x in pomiar.find():
#    print(x)
#    probki.append(x)
# return {"pomiary": probki}

@app.get('/wektor_probek/')
async def get_pomiar():
    wektory_probek = []
    for wektor_probek in wektory_probek.find():
        print(wektor_probek)
        wektor_probek.append(Wektor_Probek(**wektor_probek))
    return {"wektory_probek": wektory_probek}


@app.post('/wektor_probek/')
async def create_user(wektor_probek: Wektor_Probek):
    if hasattr(wektor_probek, 'id'):
        delattr(wektor_probek, 'id')
    ret = db_miernik.wektor_probek.insert_one(wektor_probek.dict(by_alias=True))
    wektor_probek.id = ret.inserted_id
    return {'wektor_probek': wektor_probek}


@app.get("/start_sesja/")
async def start_sesja():
    sesja_dane = {
        "data": "10.10.2021",
        "start": "True",
        "koniec": "False"
    }
    sesja = db_miernik["sesja"]
    sesje_lista = []
    x = sesja.insert_one(sesja_dane)
    print(x.inserted_id)
    y = {"": ""}
    for x in sesja.find():
        print(x)
        sesje_lista.append(x)
    return {'sesja': sesje_lista}


@app.post('/user/')
async def create_user(user: User):
    if hasattr(user, 'id'):
        delattr(user, 'id')
    ret = db_miernik.users.insert_one(user.dict(by_alias=True))
    user.id = ret.inserted_id
    return {'user': user}


@app.get('/user/')
async def get_users():
    users = []
    for user in db_miernik.users.find():
        users.append(User(**user))
    return {'users': users}


#
#
# @app.get('/user/{user_id}/')
# async def get_user():
#    # print(user_id)
#    # user = db.users.find_one({"_id": user_id})
#    # return {'user': user}
#    users = []
#    for user in db.users.find():
#        users.append(User(**user))
#    return {'users': users}
#
#
# @app.get('/user/{username}/')
# async def get_user(username: str):
#    user = db.users.find_one({"username": username})
#    return {'user': user}
#
#
# @app.post('/blog_posts/')
# async def create_blog_post(blog_post: Blog_post):
#    if hasattr(blog_post, 'id'):
#        delattr(blog_post, 'id')
#    ret = db.blog_posts.insert_one(blog_post.dict(by_alias=True))
#    blog_post.id = ret.inserted_id
#    return {"blog_post": blog_post}
#
#
# @app.get('/blog_posts/')
# async def get_blog_posts():
#    blog_posts = []
#    for blog_post in db.blog_posts.find_one():
#        blog_posts.append(Blog_post(**blog_post))
#    return {'blog_posts': blog_posts}
#
#
# @app.get('/blog_posts/{zachod_title}/')
# async def get_blog_post(zachod_title: str):
#    blog_posts = []
#    for blog_post in db.blog_posts.find_one({"title": zachod_title}):
#        blog_posts.append(Blog_post(**blog_post))
#    return {'blog_posts': blog_posts}


#    blog_post = db.blog_posts.find_one({"id": blog_post_id})
#    return {"blog_post:": blog_post}


# @app.get('/user/{id}/')
# async def put_user():

# @app.get('/user/{id}/')
# async def delete_user():

# @app.get("/blog")
# async def get_posts():
#    posts = []
#    for post in db.posts.find():
#        posts.append(User(**user))
#    return {'users': users}
#
#
# @app.get('/blog')
# async def create_post(post: Post):
#    if hasattr(post, 'id'):
#        delattr(post, 'id')
#    ret = db.posts.insert_one(post.dict(by_alias=True))
#    post.id = ret.inserted_id
#    return {'user': user}


@app.get('/')
async def read_root():
    return {'home': 'Home page'}
