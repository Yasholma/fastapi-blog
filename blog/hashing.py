from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
    def encrypt(password: str) -> str:
        return pwd_ctx.hash(password)
