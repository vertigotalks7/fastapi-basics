from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy import TIMESTAMP, text
from .database import Base

class Post(Base):
  __tablename__ = "posts"

  id = Column(Integer, primary_key=True, nullable=False)
  title = Column(String,nullable = False)
  content = Column(String, nullable=False)
  published = Column(Boolean,server_default='TRUE',default=True,nullable=False)
  created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
  owner_id = Column(Integer,ForeignKey("users.id",ondelete="cascade"),nullable=False)
class User(Base):
  __tablename__ = "users"

  id= Column(Integer, primary_key=True, nullable=False)
  email= Column(String,nullable=False,unique=True)
  password= Column(String,nullable=False)
  created_at= Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))