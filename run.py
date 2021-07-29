from fastapi import FastAPI
from models import db, User, Blog_post

app = FastAPI()


@app.post('/user/')
async def create_user(user: User):
    if hasattr(user, 'id'):
        delattr(user, 'id')
    ret = db.users.insert_one(user.dict(by_alias=True))
    user.id = ret.inserted_id
    return {'user': user}


@app.get('/user/')
async def get_users():
    users = []
    for user in db.users.find():
        users.append(User(**user))
    return {'users': users}


@app.get('/user/{user_id}/')
async def get_user():
    # print(user_id)
    # user = db.users.find_one({"_id": user_id})
    # return {'user': user}
    users = []
    for user in db.users.find():
        users.append(User(**user))
    return {'users': users}


@app.get('/user/{username}/')
async def get_user(username: str):
    user = db.users.find_one({"username": username})
    return {'user': user}


@app.post('/blog_posts/')
async def create_blog_post(blog_post: Blog_post):
    if hasattr(blog_post, 'id'):
        delattr(blog_post, 'id')
    ret = db.blog_posts.insert_one(blog_post.dict(by_alias=True))
    blog_post.id = ret.inserted_id
    return {"blog_post": blog_post}


@app.get('/blog_posts/')
async def get_blog_posts():
    blog_posts = []
    for blog_post in db.blog_posts.find_one():
        blog_posts.append(Blog_post(**blog_post))
    return {'blog_posts': blog_posts}


@app.get('/blog_posts/{zachod_title}/')
async def get_blog_post(zachod_title: str):
    blog_posts = []
    for blog_post in db.blog_posts.find_one({"title": zachod_title}):
        blog_posts.append(Blog_post(**blog_post))
    return {'blog_posts': blog_posts}


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
