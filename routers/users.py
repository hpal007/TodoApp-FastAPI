from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from sqlalchemy.orm import Session
from ..models import Todos, Users
from ..database import SessionLoacal
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix="/users", tags=["users"]
)


def get_db():
    db = SessionLoacal()
    try:
        yield db
    finally:
        db.close()


# dependency injection
db_dependency = Annotated[Session, Depends(get_db)]
user_depencncy = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserVerification(BaseModel):
    password:str
    new_password:str = Field(min_length=6)

class UpdatePhoneNumber(BaseModel):
    phone_number:str

@router.get("/",status_code=status.HTTP_200_OK)
async def get_user(user: user_depencncy,db: db_dependency):

    # check auth
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed."
        )
    
    return db.query(Users).filter(Users.id == user.get('user_id')).first()


@router.put("/password",status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_depencncy,
                          db: db_dependency,
                          user_varification:UserVerification):

    # check auth
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed."
        )
    
    user_model = db.query(Users).filter(Users.id == user.get("user_id")).first()
    if not bcrypt_context.verify(user_varification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_password = bcrypt_context.hash(user_varification.new_password)
    db.add(user_model)
    db.commit()


@router.put("/phone_number",status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(user: user_depencncy,
                          db: db_dependency,
                          phone_number:UpdatePhoneNumber):

    # check auth
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed."
        )
    
    user_model = db.query(Users).filter(Users.id == user.get("user_id")).first()

    user_model.phone_numer = phone_number.phone_number
    db.add(user_model)
    db.commit()


@router.get("/users")
async def get_users(db: db_dependency):

    
    users = db.query(Users).all()
    return users



# pg password: test1234!