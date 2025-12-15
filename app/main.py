from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
  title: str
  content: str
  published: bool = True
  rating: Optional[int] = None


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

##----------- display all 

@app.get("/posts")
def get_posts():
  return {"data":my_posts};

##---------------- creation of post

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
  post_dict=post.model_dump()
  post_dict["id"]=randrange(0,1000000)
  my_posts.append(post_dict)
  return {"data":post_dict}; 

#title str, content str,category,bool idk idk


#---------------- search posts (last index is the latest post) lolz
@app.get("/posts/latest")
def get_latest_post():
  lpost = my_posts[-1]
  return {"the latest post is":lpost}

#---------------- get post by id linear search.

@app.get("/posts/{id}")
def get_post_each(id:int):


  fpost = find_post_byid(id);
  if not fpost:
   #res.status_code = status.HTTP_404_NOT_FOUND;
   #return{"message":f"post with {id} is not found"};
   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"pst with invalid id")
  print(id);
  return {"post_detail":fpost};


##----------deletion of post by id linear search

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
  #delte post
  #finding index through linear search
  index = find_index_post(id);

  if index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
  
  my_posts.pop(index)
  return Response(status_code=status.HTTP_204_NO_CONTENT);

##---------- update post by id linear search

@app.put("/posts/{id}")
def update_post(id: int,post: Post):

  index = find_index_post(id);

  if index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
  
  post_dict = post.model_dump()
  post_dict['id'] = id
  my_posts[index] = post_dict
  return{"data":post_dict};