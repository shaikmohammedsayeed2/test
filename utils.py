from sqlalchemy.orm import Session
from database import SessionLocal
import models


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    