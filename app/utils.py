from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["argon2"],deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)