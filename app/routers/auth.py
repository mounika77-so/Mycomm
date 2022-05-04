from fastapi import Depends, FastAPI, Response, status, HTTPException, Depends, APIRouter, Request
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter(tags=["Authentication"])


@router.post('/login', response_model=schemas.Token)
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.admin).filter(
        models.admin.email == user_cred.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid")

    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="wrong password")

    access_token = oauth2.create_access_token_user(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "Bearer"}


@router.post('/ulogin', response_model=schemas.Token)
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.user).filter(
        models.user.email == user_cred.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid")

    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="wrong password")

    access_token = oauth2.create_access_token_user(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "Bearer"}
