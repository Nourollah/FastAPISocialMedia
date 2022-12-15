from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database, models, oauth2, schemas

router = APIRouter(
    prefix="/votes",
    tags=["Vote"]
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote,
         db: Session = Depends(database.get_db),
         current_user: schemas.UserLogin = Depends(oauth2.get_current_user)):

    post_check = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()
    if not post_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} Not found")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.direction == 1:
        if found_vote:
            if found_vote.direction == 1:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail="You already voted this post")
            else:
                found_vote.direction = 1
        else:
            new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message": "Successfully voted"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully unvoted"}