from fastapi import FastAPI
from app import models
from .database import ENGINE
from .routers import post,user,auth,vote
from .config import settings

app = FastAPI()

models.Base.metadata.create_all(bind=ENGINE)
    
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

##------------- fastapi url test

@app.get("/")
async def root():
  return {"message":"my name  is angelo"};

















# request get method url: "/"
#also order mattters when writing larger codes with multiple links
#also if the linking is same it takes the first one itt sees (searches from top to bottom)


##--------- dummy case for postman
# my_posts = [{"title":"title of post 1","content":"content of post 1","id":1},{"title":"fav foods","content":"i like pizza","id":2}]


# ##--------------- ffff start
# def find_post_byid(id):
#   for p in my_posts:
#     if p["id"]==id:
#       return p

# def find_index_post(id):
#   for i,p in enumerate(my_posts):
#     if p['id'] == id:
#       return i

##---------------- ORM 1st test

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#   posts = db.query(models.Post)
#   print(posts)
#   return {"data":"s"}


