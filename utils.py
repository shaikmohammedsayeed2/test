from sqlalchemy.orm import Session
from database import SessionLocal
import models
from session import get_rle_session, RleSession, HTTPException
from fastapi import Request


PERSON_ROLE = {"student" : 1,"faculty" : 2,"staff" : 3,"sponsor":4}
USER_ROLE = {"admin":1,"manager":2,"user":3}


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_session(request:Request):
    return get_rle_session(request)


async def insert_into_binary_table(db:Session, url:str):
    bin_entry = models.Binary(
        blob_storage = url,
        is_active = True,
        # blob_size = -1,
        #created_by = 1      ##TODO: Insert logeed in perosn id
    )
    db.add(bin_entry)
    db.commit()
    db.refresh(bin_entry)

    return bin_entry.id

def get_role_name_by_id(role_id):
    if role_id ==1:
        return "admin"
    elif role_id ==3:
        return "user"
    elif role_id ==2:
        return "manager"
    
def CHECK_ACCESS(user:RleSession, MIN_ACCESS_LEVEL:int):
    return True
    if user.valid == False or user.role_id > MIN_ACCESS_LEVEL:
        print(user, "Required Access Level: ", MIN_ACCESS_LEVEL)
        raise HTTPException(status_code=401, detail="Unauthorized")
