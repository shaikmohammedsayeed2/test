from fastapi import Depends, APIRouter,HTTPException
from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy import text
from pathlib import Path
from utils import get_db, insert_into_binary_table

router = APIRouter()

PERSON_ROLE = {"student" : 1,"faculty" : 2,"staff" : 3,"sponsor":4}
USER_ROLE = {"admin":1,"user":2,"manager":3}


## Function to get the members of the given lab
@router.get("/people/{lab_id}")
async def get_people(lab_id:int, db: Session = Depends(get_db)):
    sql = text(Path("sql/people.sql").read_text().format(lab_id))
    results = db.execute(sql)
    return results.mappings().all()


@router.post("/person")
async def add_person(person: schemas.PersonAdd ,db: Session = Depends(get_db)):
    # Checks 
    try:
        assert person.person_role.lower() in PERSON_ROLE.keys() 
        assert person.user_role.lower() in USER_ROLE.keys() 
    except AssertionError:
        raise HTTPException(status_code=422, detail="Person role argument invalid")
    
    

    person_bin_id = await insert_into_binary_table(db,person.person_image)

    ## Person Table entry
    person_entry = models.Person(
        name = person.name,
        roll_number = person.roll_number,
        linkedin_url = person.linkedin_url,
        github_url = person.github_url,
        personal_web_url = person.personal_web_url,
        profile_binary_id = person_bin_id,
        is_active = True,
        #created_by = 1##TODO: Insert logeed in perosn id
    )

    db.add(person_entry)
    db.commit()
    db.refresh(person_entry)

    

    ## Lab Member table entry
    lab_mem_entry = models.LabMember(
        person_id = person_entry.id,
        lab_id= person.lab_id,
        role_id = USER_ROLE[person.user_role],
        person_role_id = PERSON_ROLE[person.person_role]

    )

    db.add(lab_mem_entry)
    db.commit()
    db.refresh(lab_mem_entry)

    return person_entry.id


## to delete a person
@router.delete("/person")
async def delete_labmember_by_id(labmember_id:int,db: Session = Depends(get_db)):
    person_id = db.get(models.LabMember,labmember_id).person_id
    ref_count = db.query(models.Person).filter(models.Person.id==person_id).count()
    if ref_count == 1:
        db.delete(db.get(models.Person,person_id))
    else:
        db.delete(db.get(models.LabMember,labmember_id))
    db.commit()
    return ""  
