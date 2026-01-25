from app import models, schemas, utils
from fastapi import FastAPI,Response,status,HTTPException, Depends, APIRouter
from app.database import ENGINE , get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#-------------OPERATIONS ON USERS TABLE

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Userout)
def create_user(user: schemas.UserCreate ,db: Session = Depends(get_db)):

  #hashing the password - user.password
  hashed_password = utils.hash_password(user.password)
  user.password = hashed_password

  new_user = models.User(**user.model_dump())
  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  return new_user

@router.get("/{id}",response_model=schemas.Userout)
def get_user(id: int,db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with invalid id")
  return user