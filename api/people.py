from fastapi import Depends, APIRouter,HTTPException
from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy import text
from pathlib import Path
from utils import *
from session import RleSession

router = APIRouter()



## Function to get the members of the given lab
@router.get("/people/{lab_id}")
async def get_people(lab_id:int, user:RleSession = Depends(get_session), db:Session = Depends(get_db)):
    sql = text(Path("sql/people.sql").read_text().format(lab_id))
    results = db.execute(sql)
    return results.mappings().all()

## Function to get the person using person_id
@router.get("/person/{person_id}")
async def get_person(person_id:int, user:RleSession = Depends(get_session), db:Session = Depends(get_db)):
    response = dict()
    person = db.get(models.Person,person_id)
    response['person'] = person
    person_image = db.get(models.Binary,person.profile_binary_id).blob_storage
    response['person_image'] = person_image
    return response


@router.post("/person")
async def add_person(person: schemas.PersonAdd ,user:RleSession = Depends(get_session), db:Session = Depends(get_db)):
    
    CHECK_ACCESS(user, USER_ROLE["manager"])

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
async def delete_labmember_by_id(labmember_id:int,user:RleSession = Depends(get_session), db:Session = Depends(get_db)):
    
    CHECK_ACCESS(user, USER_ROLE["manager"])

    person_id = db.get(models.LabMember,labmember_id).person_id
    ref_count = db.query(models.Person).filter(models.Person.id==person_id).count()
    if ref_count == 1:
        db.delete(db.get(models.Person,person_id))
    else:
        db.delete(db.get(models.LabMember,labmember_id))
    db.commit()
    return ""  

## to update a person
@router.put("/person/{person_id}")
async def update_person(person_id:int,person: schemas.PersonUpdate ,user:RleSession = Depends(get_session), db:Session = Depends(get_db)):
    
    CHECK_ACCESS(user, USER_ROLE["user"])

    # Allow the person to edit his data only
    if user.role_id==USER_ROLE["user"] and person_id != user.person_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    db_item = db.query(models.Person).filter(models.Person.id==person_id).first()
    db_blob_storage = db.query(models.Binary).filter(models.Binary.id == db_item.profile_binary_id).first()
    db_lab_member = db.query(models.LabMember).filter(models.LabMember.person_id == person_id).first()
    if not db_item:
        return {"error":"Item not found"}
    
    if person.person_image:
        db_blob_storage.blob_storage = person.person_image

    update_person_data = {k: v for k, v in person.dict(exclude_unset=True).items()}
    for key, value in update_person_data.items():
        setattr(db_item, key, value)
    
    if person.lab_id:
        db_lab_member.lab_id = person.lab_id
    
    if person.person_role:
        db_lab_member.person_role_id = PERSON_ROLE[person.person_role]
    
    if person.user_role:
        db_lab_member.role_id = USER_ROLE[person.user_role]           

    db.commit()

    return "Success"