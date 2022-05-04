import re
from fastapi import Depends, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db
import calendar
import datetime

router = APIRouter(
    prefix="/user",
    tags=['User'])


@router.post("/user_create", status_code=status.HTTP_201_CREATED, response_model=schemas.user)
async def acreate(user: schemas.user, db: Session = Depends(get_db)):
    # hast the password - user.password

    hasdhed_password = utils.hash(user.password)
    user.password = hasdhed_password

    new_user = models.user(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/get_users')
def get_users(db: Session = Depends(get_db)):
    user = db.query(models.user).all()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user not found")

    return user


@router.get('/get_user{phone}', response_model=schemas.user)
def get_users(phone: int, db: Session = Depends(get_db)):
    user = db.query(models.user).filter(
        models.admin.phone == phone).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with phone: {phone} not found")

    return user


@router.delete("/user_delete", status_code=status.HTTP_204_NO_CONTENT)
async def udelete(phone: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_admin)):
    post_q = db.query(models.user).filter(models.user.phone == phone)
    post = post_q.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")
    post_q.delete(synchronize_session=False)
    db.commit()
    return "successfully deleted"


@router.put("/admin{phone}", status_code=status.HTTP_202_ACCEPTED)
async def update_admin(phone: int, user: schemas.admin, db: Session = Depends(get_db)):
    bay_q = db.query(models.user).filter(models.user.phone == phone)
    bay = bay_q.first()

    if phone == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found")

    bay_q.update(user.dict(), synchronize_session=False)
    db.commit()
