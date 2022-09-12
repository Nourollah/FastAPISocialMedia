from jose import jwt, JWTError
import datetime
from fastapi import Depends, HTTPException, status, security
from sqlalchemy import orm

from . import schemas, database, models

from .config import settings

oauth2_schemas = security.OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode['exp'] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        idx: str = payload.get('user_id')

        if idx is None:
            raise credentials_exception

        token_data = schemas.TokenData(idx=idx)

    except JWTError as e:
        raise credentials_exception from e

    return token_data


def get_current_user(token: str = Depends(oauth2_schemas),
                     db: orm.Session = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate user credentials",
                                          headers={'WWW-Authenticate': f'Bearer {token}'})

    token = verify_access_token(token, credentials_exception)
    return db.query(models.Users).filter(models.Users.id == token.idx).first()

