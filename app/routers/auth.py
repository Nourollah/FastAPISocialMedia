from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import orm
from fastapi.security import OAuth2PasswordRequestForm

from .. import models, schemas, database, utils, oauth2


router = APIRouter(
    prefix="/login",
    tags=["Login"]
)


@router.post('/', status_code=status.HTTP_202_ACCEPTED)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: orm.Session = Depends(database.get_db)):
    try:
        user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
        http_response_message = "Authentication failed"
        if user is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=http_response_message)
        if not utils.verify_pass(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=http_response_message)

        access_token = oauth2.create_access_token(data={"user_id": user.id})
        return {"token": access_token,
                "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Authentication failed") from e
