from fastapi import FastAPI,Response,status,HTTPException, Depends
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from app import models,schemas,utils
from app.database import ENGINE , get_db
from sqlalchemy.orm import Session
from app.routers import post,user

app = FastAPI()
models.Base.metadata.create_all(bind=ENGINE)

while True:
  try:
    conn = psycopg2.connect(host='localhost',database='fastapi_db',user='postgres', password='2006',cursor_factory=RealDictCursor)

    cursor = conn.cursor();
    print("database connection successful")
    break

  except Exception as e:
    print("connection to database failed")
    time.sleep(2)
    conn.close()


# request get method url: "/"
#also order mattters when writing larger codes with multiple links
#also if the linking is same it takes the first one itt sees (searches from top to bottom)


##--------- dummy case for postman
my_posts = [{"title":"title of post 1","content":"content of post 1","id":1},{"title":"fav foods","content":"i like pizza","id":2}]


##--------------- ffff start
def find_post_byid(id):
  for p in my_posts:
    if p["id"]==id:
      return p

def find_index_post(id):
  for i,p in enumerate(my_posts):
    if p['id'] == id:
      return i
    
app.include_router(post.router)
app.include_router(user.router)

##------------- fastapi url test

@app.get("/")
async def root():
  return {"message":"my name  is angelo"};
##---------------- ORM 1st test

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#   posts = db.query(models.Post)
#   print(posts)
#   return {"data":"s"}


