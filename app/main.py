from fastapi import FastAPI,Response,status,HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from app import models
from app.database import ENGINE , get_db
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=ENGINE)


class Post(BaseModel):
  title: str
  content: str
  published: bool = True


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
    

##------------- fastapi url test

@app.get("/")
async def root():
  return {"message":"my name  is angelo"};
##---------------- ORM 1st test

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
  posts = db.query(models.Post)
  print(posts)
  return {"data":"s"}


##----------- display all 

@app.get("/posts")
def get_posts():
  cursor.execute("""SELECT * FROM posts""")
  posts=cursor.fetchall()
  return {"data":posts};

##---------------- creation of post

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
  cursor.execute(("""INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) RETURNING * """),(post.title,post.content,post.published))
  new_post =cursor.fetchone() 
  conn.commit()

  return {"data":new_post}; 

#title str, content str,category,bool idk idk


#---------------- search posts (last index is the latest post) lolz
@app.get("/posts/latest")
def get_latest_post():
  lpost = my_posts[-1]
  return {"the latest post is":lpost}

#---------------- get post by id linear search.

@app.get("/posts/{id}")
def get_post_each(id:int):
  cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id)))
  fpost = cursor.fetchone()
  if not fpost:
   #res.status_code = status.HTTP_404_NOT_FOUND;
   #return{"message":f"post with {id} is not found"};
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with invalid id")
  return {"post_detail":fpost};


##----------deletion of post

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
  cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
  deleted_post = cursor.fetchone()
  conn.commit()

  if deleted_post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")

  return Response(status_code=status.HTTP_204_NO_CONTENT);

##---------- update post by id linear search

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts 
           SET title = %s, content = %s, published = %s 
           WHERE id = %s 
           RETURNING *""",
        (post.title, post.content, post.published, id)  # keep id as int
    )

    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:  # check the result, not the function
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    return {"data": updated_post}
