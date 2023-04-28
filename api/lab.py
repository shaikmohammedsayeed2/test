from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import models, schemas
from utils import get_db, insert_into_binary_table

router = APIRouter()


@router.get("/labs", response_model=list[schemas.Lab])
async def read_users(db: Session = Depends(get_db)):
    labs = db.query(models.Lab).all()
    print(labs)
    return labs


## New lab creation
@router.post("/lab")
async def create_lab(lab: schemas.LabAdd ,db: Session = Depends(get_db)):
    ## Insert into Binary table 
    lab_logo_bin_id = await insert_into_binary_table(db,lab.lab_logo_url)
    lab_cover_bin_id = await insert_into_binary_table(db,lab.lab_cover_url)

    ## Contact Us table entry
    contact_entry = models.ContactUs(
        address = lab.address,
        email = lab.email,
        phone = lab.phone,
        is_active = True,
        #created_by = 1##TODO: Insert logeed in perosn id
    )

    db.add(contact_entry)
    db.commit()
    db.refresh(contact_entry)

    ## Lab Table entry
    lab_entry = models.Lab(
        name = lab.name,
        lab_logo_id = lab_logo_bin_id,
        cover_binary_id = lab_cover_bin_id,
        overview = lab.overview,
        contact_id = contact_entry.id,
        twitter_handle = lab.twitter_handle,
        is_active = True,
        #created_by = 1##TODO: Insert logeed in perosn id
    )

    db.add(lab_entry)
    db.commit()
    db.refresh(lab_entry)

    return lab_entry.id

## to delete a lab
@router.delete("/lab")
async def delete_lab_by_id(lab_id:int,db: Session = Depends(get_db)):
    lab = db.get(models.Lab,lab_id)
    contactus = db.get(models.ContactUs,lab.contact_id) 
    db.delete(lab)
    db.delete(contactus)
    db.commit()
    return ""

## New ContactUs Creation
@router.post("/contactus")
async def add_contactus(contact: schemas.ContactUsAdd ,db: Session = Depends(get_db)):
    ## ContactUs Table entry
    contactus_entry = models.ContactUs(
        address = contact.address,
        email = contact.email,
        phone = contact.phone,
        is_active = True,
        #created_by = 1##TODO: Insert logeed in perosn id
    )

    db.add(contactus_entry)
    db.commit()
    db.refresh(contactus_entry)

    return contactus_entry.id



