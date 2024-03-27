from datetime import timedelta, datetime

from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from dotenv import load_dotenv, find_dotenv
import os

from pymongo import MongoClient

from config.db import get_collection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

_ = load_dotenv(find_dotenv())

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_user_collection():
    client = MongoClient("mongodb://localhost:27017")
    db = client["lead_compass"]
    user_collection = db["user"]
    return user_collection


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt


def verify_token_access(token: str):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="You Are Not Authorized",
                                          headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
    except JWTError as e:
        print(e)
        raise credentials_exception

    return payload


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        user_collection = get_user_collection()
        token = verify_token_access(token)
        user_id = token.get('user_id')

        if user_id is not None:
            user_id = ObjectId(user_id)
            user = user_collection.find_one({"_id": user_id})
            if user:
                user["_id"] = str(user["_id"])
                return user
            else:
                raise HTTPException(status_code=404, detail='Invalid token, No user found')
        else:
            raise HTTPException(status_code=401, detail='Invalid token')

    except HTTPException as http_exception:
        raise http_exception

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'error: {str(e)}')
