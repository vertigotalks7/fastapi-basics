from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import database ,schemas, models, utils,OAuth2

router = APIRouter(tags=["Authentication"]) 

@router.post("/login",response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    # create a token
    # return token
    access_token = OAuth2.create_access_token(data = {"user_id":user.id})
    return {"access_token": access_token,"token_type":"bearer"}


#debugging endpoint to check the silly auth error that i am getting when trying to access the protected route with the token generated from the login endpoint. it is giving me an error that says "Could not validate credentials" even though the token is correct and valid. so this endpoint will help me check if the token is being generated correctly and if it can be decoded correctly. if this endpoint works then the problem is with the protected route and not with the token generation or decoding.
@router.get("/debug-token")
def debug_token(token: str = Depends(OAuth2.oauth2_scheme)):
    """Temporary debug endpoint: returns the raw token and decoded payload.
    Do not expose in production. Call with Authorization: Bearer <token>."""
    try:
        payload = jwt.decode(token, OAuth2.SECRET_KEY, algorithms=[OAuth2.ALGORITHIM])
        return {"token": token, "payload": payload}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

