from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas

from sqlalchemy import select,text

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/labs", response_model=list[schemas.Lab])
async def read_users(db: Session = Depends(get_db)):
    labs = db.query(models.Lab).all()
    print(labs)
    return labs


## Function to get the members of the given lab

@app.get("/people/{lab_id}")
async def get_people(lab_id:int, db: Session = Depends(get_db)):
    sql = text()
    results = db.execute(sql)
    print(results)

    return results.mappings().all()
