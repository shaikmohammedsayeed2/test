from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import models, schemas
from utils import get_db, insert_into_binary_table
from sqlalchemy import text
from pathlib import Path
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


## to delete a lab - Completed
@router.delete("/lab")
async def delete_lab_by_id(lab_id:int,db: Session = Depends(get_db)):
    lab = db.get(models.Lab,lab_id)
    contactus = db.get(models.ContactUs,lab.contact_id)
    logo_image = db.get(models.Binary,lab.lab_logo_id)
    cover_image = db.get(models.Binary,lab.cover_binary_id) 
    
    sql = text(Path("sql/delete_lab.sql").read_text().format(lab_id))
    
    db.delete(lab)
    db.delete(contactus)
    db.delete(logo_image)
    db.delete(cover_image)
    db.execute(sql)
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


## To Update A Lab
@router.put("/lab/{lab_id}")
async def update_lab(lab_id:int,lab: schemas.LabUpdate ,db: Session=Depends(get_db)):
    
    db_item = db.query(models.Lab).filter(models.Lab.id==lab_id).first()
    db_contact = db.query(models.ContactUs).filter(models.ContactUs.id == db_item.contact_id).first()
    if not db_item:
        return {"error":"Item not found"}

    if lab.lab_logo_url:
        db_lab_logo_binary = db.query(models.Binary).filter(models.Binary.id==db_item.lab_logo_id).first()
        db_lab_logo_binary.blob_storage = lab.lab_logo_url

    if lab.lab_cover_url:
        db_lab_cover_binary = db.query(models.Binary).filter(models.Binary.id==db_item.cover_binary_id).first()
        db_lab_cover_binary.blob_storage = lab.lab_cover_url    
    

    update_lab_data = {k: v for k, v in lab.dict(exclude_unset=True).items()}
    for key, value in update_lab_data.items():
        setattr(db_item, key, value)
        
    
    update_contact_data = {k: v for k, v in lab.dict(exclude_unset=True).items()}
    for key, value in update_contact_data.items():
        setattr(db_contact, key, value)    

    db.commit()

    return "Success"


