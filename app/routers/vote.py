from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, database, oauth2

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_404_NOT_FOUND)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    real_estate = db.query(models.RealEstate).filter(
        models.RealEstate.id == vote.real_estate_id).first()

    if not real_estate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Real estate with id {vote.real_estate_id} does not exist")

    vote_query = db.query(models.Vote).filter(
        models.Vote.real_estate_id == vote.real_estate_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on real estate {vote.real_estate_id}")
        new_vote = models.Vote(
            real_estate_id=vote.real_estate_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}
