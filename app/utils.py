from passlib.context import CryptContext
# Use bcrypt_sha256 to avoid the 72-byte bcrypt limit (it pre-hashes with SHA256)
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)