from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import orm

from .. import database, models, schemas, utils

router = APIRouter(
    prefix="/users",
    tags=["User"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserShow)
async def post_user(user: schemas.UserCreate,
                    db: orm.Session = Depends(database.get_db)):
    user.password = utils.make_hash(user.password)

    new_user = models.Users(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{idx}', response_model=schemas.UserShow)
async def get_user(idx: int,
                   db: orm.Session = Depends(database.get_db)):
    try:
        return db.query(models.Users).filter(models.Users.id == idx).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {idx} Not found") from e
