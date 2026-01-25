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


##----------- display all 

@app.get("/posts",response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):

  # cursor.execute("""SELECT * FROM posts""")
  # posts=cursor.fetchall()

  posts = db.query(models.Post).all()
  return posts

##---------------- creation of post

@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):

  # cursor.execute(("""INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) RETURNING * """),(post.title,post.content,post.published))
  # new_post =cursor.fetchone() 
  # conn.commit()

  print(post.model_dump())
  new_post = models.Post(**post.model_dump())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)

  return new_post

#title str, content str,category,bool idk idk


#---------------- search posts (last index is the latest post) lolz
@app.get("/posts/latest")
def get_latest_post():
  lpost = my_posts[-1]
  return {"the latest post is":lpost}

#---------------- get post by id linear search.

@app.get("/posts/{id}",response_model=schemas.Post)
def get_post_each(id:int,db: Session = Depends(get_db)):

  post = db.query(models.Post).filter(models.Post.id == id).first()
  print(post)

  #cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id)))
  #fpost = cursor.fetchone()

  if not post:
                                      #res.status_code = status.HTTP_404_NOT_FOUND;
                                      #return{"message":f"post with {id} is not found"};
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with invalid id")
  return post


##----------deletion of post

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int,db: Session = Depends(get_db)):
  
  post = db.query(models.Post).filter(models.Post.id == id)

  #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
  #deleted_post = cursor.fetchone()
  #conn.commit()

  if post.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
  
  post.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)

##---------- update post by id linear search

@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,db: Session = Depends(get_db)):
    
    post_query= db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    # cursor.execute(
    #     """UPDATE posts 
    #        SET title = %s, content = %s, published = %s 
    #        WHERE id = %s 
    #        RETURNING *""",
    #     (post.title, post.content, post.published, id)  # keep id as int
    # )

    # updated_post = cursor.fetchone()
    # conn.commit()

    if post is None:  # check the result, not the function
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()

    return post_query.first()

#-------------OPERATIONS ON USERS TABLE

@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.Userout)
def create_user(user: schemas.UserCreate ,db: Session = Depends(get_db)):

  #hashing the password - user.password
  hashed_password = utils.hash_password(user.password)
  user.password = hashed_password

  new_user = models.User(**user.model_dump())
  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  return new_user
