from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy import text
from pathlib import Path
from utils import get_db, insert_into_binary_table

router = APIRouter()



@router.get("/publications/{lab_id}")
async def get_publications(lab_id:int, db: Session = Depends(get_db)):
    sql = text(Path("sql/publications.sql").read_text().format(lab_id))
    results = db.execute(sql)
    return results.mappings().all()

@router.get("/conferences/{lab_id}")
async def get_publications(lab_id:int, db: Session = Depends(get_db)):
    sql = text(Path("sql/conference.sql").read_text().format(lab_id))
    results = db.execute(sql)
    return results.mappings().all()


@router.get("/research/{lab_id}")
async def get_publications(lab_id:int, db: Session = Depends(get_db)):
    sql = text(Path("sql/conference.sql").read_text().format(lab_id))
    results = db.execute(sql)
    return results.mappings().all()



@router.post("/publication")
async def add_publication(pub: schemas.PublicationAdd ,db: Session = Depends(get_db)):
     ## Insert into Binary table 
    publication_bin_id = await insert_into_binary_table(db,pub.pub_pdf)

    ## Publication Table entry
    publication_entry = models.Publication(
        pub_title = pub.pub_title,
        pub_binary_id = publication_bin_id,
        pub_date = pub.pub_date,
        description = pub.description,
        lab_id = pub.lab_id,
        type = pub.type,
        #created_by = 1##TODO: Insert logeed in perosn id
    )

    db.add(publication_entry)
    db.commit()
    db.refresh(publication_entry)

    return publication_entry.id




@router.post("/conference")
async def add_conference(conf: schemas.ConferenceAdd ,db: Session = Depends(get_db)):
    ## Insert into Binary table 
    conference_bin_id = await insert_into_binary_table(db,conf.conf_pdf)

    ## Publication Table entry
    conference_entry = models.Conference(
        conf_title = conf.conf_title,
        conf_binary_id = conference_bin_id,
        description = conf.description,

        start_date = conf.start_date,
        end_date = conf.end_date,

        lab_id = conf.lab_id,
        is_active = conf.is_active,
        #created_by = 1##TODO: Insert logeed in perosn id
    )

    db.add(conference_entry)
    db.commit()
    db.refresh(conference_entry)

    return conference_entry.id


@router.post("/patent")
async def add_patent(patent: schemas.PatentAdd ,db: Session = Depends(get_db)):
    ## Patent Table entry
    patent_entry = models.Patent(
        publication_id = patent.publication_id,
        description = patent.description,
        lab_id = patent.lab_id,
        is_active = True,
        #created_by = 1##TODO: Insert logeed in perosn id
    )

    db.add(patent_entry)
    db.commit()
    db.refresh(patent_entry)

    return patent_entry.id


## to delete a lab
@router.delete("/conference")
async def delete_conference_by_id(conf_id:int,db: Session = Depends(get_db)):
    db.delete(db.get(models.Conference,conf_id))
    db.commit()
    return "" 


## to delete a publication
@router.delete("/publication")
async def delete_publication_by_id(publication_id:int,db: Session = Depends(get_db)):
    db.delete(db.get(models.Publication,publication_id))
    db.commit()
    return ""

## to delete a patent
@router.delete("/patent")
async def delete_patent_by_id(patent_id:int,db: Session = Depends(get_db)):
    db.delete(db.get(models.Patent,patent_id))
    db.commit()
    return ""