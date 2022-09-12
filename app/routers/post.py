from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import orm
from typing import List, Optional

from .. import models, schemas, database, oauth2

router = APIRouter(
    prefix='/posts',
    tags=['Post'],
)


@router.get("/", response_model=List[schemas.Post])
async def get_posts(db: orm.Session = Depends(database.get_db),
                    current_user: schemas.UserLogin = Depends(oauth2.get_current_user),
                    limit: int = 10,
                    skip: int = 0,
                    search: Optional[str] = ''):
    return db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()


@router.get("/{idx}", response_model=schemas.Post)
async def get_one_posts(idx: int,
                        db: orm.Session = Depends(database.get_db),
                        current_user: schemas.UserLogin = Depends(oauth2.get_current_user)):
    return db.query(models.Posts).filter(models.Posts.id == idx).first()

@router.get("/{idx}", response_model=schemas.Post)
async def get_user_posts(idx: int,
                        db: orm.Session = Depends(database.get_db),
                        current_user: schemas.UserLogin = Depends(oauth2.get_current_user)):

    posts = db.query(models.Posts).filter(models.Posts.owner_id == current_user.id).all()

    if posts.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You don't have permission to access this item")
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def post_item(payload: schemas.PostCreate,
                    db: orm.Session = Depends(database.get_db),
                    current_user: schemas.UserLogin = Depends(oauth2.get_current_user)):

    new_post = models.Posts(owner_id=current_user.id, **payload.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put('/{idx}', status_code=status.HTTP_200_OK, response_model=schemas.Post)
async def update_item(idx: int,
                      post: schemas.PostCreate,
                      db: orm.Session = Depends(database.get_db),
                      current_user: schemas.UserLogin = Depends(oauth2.get_current_user)):
    item_query = db.query(models.Posts).filter(models.Posts.id == idx)
    item = item_query.first()

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"id {idx} Not found")
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You don't have permission to access this item")

    item_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return item


@router.delete('/{idx}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(idx: int,
                      db: orm.Session = Depends(database.get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    item_query = db.query(models.Posts).filter(models.Posts.id == idx)

    post = item_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"id {idx} Not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You do not have permission to delete this post")

    item_query.delete(synchronize_session=False)
    db.commit()
