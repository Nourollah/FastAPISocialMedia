from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def make_hash(password: str):
    return pwd_context.hash(password)


def verify_pass(plain_text_pass: str, hashed_pass: str):
    return pwd_context.verify(plain_text_pass, hashed_pass)
