from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func
from .. import models, schemas, oauth2

router = APIRouter(prefix="/realestates", tags=["Real Estates"])


# @router.get("/", response_model=List[schemas.RealEstate])
@router.get("/", response_model=List[schemas.RealEstateOut])
def get_all_real_estates(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 15, skip: int = 0, search: Optional[str] = ""):

    # real_estates = db.query(models.RealEstate).filter(
    #     models.RealEstate.name.contains(search)).limit(limit).offset(skip).all()

    real_estates = db.query(models.RealEstate, func.count(models.Vote.real_estate_id).label("votes")).join(
        models.Vote, models.Vote.real_estate_id == models.RealEstate.id, isouter=True).group_by(models.RealEstate.id).filter(
        models.RealEstate.name.contains(search)).limit(limit).offset(skip).all()
    return real_estates


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.RealEstate)
def create_real_estates(real_estate: schemas.RealEstateCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO real_estates (name, description, price) VALUES (%s, %s, %s) RETURNING * """,
    #                (real_estate.name, real_estate.description, real_estate.price))
    # new_real_estate = cursor.fetchone()

    # conn.commit()
    new_real_estate = models.RealEstate(
        owner_id=current_user.id, **real_estate.dict())
    db.add(new_real_estate)
    db.commit()
    db.refresh(new_real_estate)
    return new_real_estate


@router.get("/{id}", response_model=schemas.RealEstateOut)
def get_one_real_estate(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM real_estates WHERE id = %s """, (str(id)))
    # real_estate = cursor.fetchone()

    real_estate = db.query(models.RealEstate, func.count(models.Vote.real_estate_id).label("votes")).join(
        models.Vote, models.Vote.real_estate_id == models.RealEstate.id, isouter=True).group_by(models.RealEstate.id).filter(
        models.RealEstate.id == id).first()
    if not real_estate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"real estate with id: {id} was not found")

    return real_estate


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_real_estate(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """DELETE FROM real_estates WHERE id = %s RETURNING *""", (str(id)))
    # deleted_real_estate = cursor.fetchone()

    # conn.commit()
    real_estate_query = db.query(models.RealEstate).filter(
        models.RealEstate.id == id)

    real_estate = real_estate_query.first()

    if real_estate == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"real estate with id: {id} does not exist")

    if real_estate.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    real_estate_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.RealEstate)
def update_real_estate(id: int, updated_real_estate: schemas.RealEstateCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE real_estates SET name = %s, description = %s, price = %s WHERE id = %s RETURNING *""",
    #                (real_estate.name, real_estate.description, real_estate.price, str(id)))
    # updated_real_estate = cursor.fetchone()

    # conn.commit()

    real_estate_query = db.query(models.RealEstate).filter(
        models.RealEstate.id == id)

    real_estate = real_estate_query.first()

    if real_estate == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exist")

    if real_estate.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    real_estate_query.update(updated_real_estate.dict(),
                             synchronize_session=False)
    db.commit()
    return real_estate_query.first()
