from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Encrypting():
    def encryptPassword(password: str):
        return pwd_context.hash(password)

    def checkEncryptedPassword(encrypted, plainPassword):
        return pwd_context.verify(plainPassword, encrypted)