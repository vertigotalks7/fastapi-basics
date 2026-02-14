from app import models, schemas, utils ,OAuth2
from fastapi import FastAPI,Response,status,HTTPException, Depends, APIRouter
from app.database import ENGINE , get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

##----------- display all 

@router.get("/",response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):

  # cursor.execute("""SELECT * FROM posts""")
  # posts=cursor.fetchall()

  posts = db.query(models.Post).all()
  return posts

##---------------- creation of post

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(OAuth2.get_current_user)):

  # cursor.execute(("""INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) RETURNING * """),(post.title,post.content,post.published))
  # new_post =cursor.fetchone() 
  # conn.commit()
  print(user_id)
  print(post.model_dump())
  new_post = models.Post(**post.model_dump())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)

  return new_post

#title str, content str,category,bool idk idk


#---------------- search posts (last index is the latest post) lolz

# @router.get("/posts/latest")
# def get_latest_post():
#   lpost = my_posts[-1]
#   return {"the latest post is":lpost}

#---------------- get post by id linear search.

@router.get("/{id}",response_model=schemas.Post)
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

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int,db: Session = Depends(get_db),user_id: int = Depends(OAuth2.get_current_user)):
  
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

@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,db: Session = Depends(get_db),user_id: int = Depends(OAuth2.get_current_user)):
    
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