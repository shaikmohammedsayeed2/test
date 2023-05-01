from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy import text
from pathlib import Path
from utils import *
from session import RleSession


router = APIRouter()



@router.get("/publications/{lab_id}")
async def get_publications(lab_id:int, user:RleSession = Depends(get_session), db:Session = Depends(get_db)):
    sql = text(Path("sql/publications.sql").read_text().format(lab_id))
    results = db.execute(sql)
    return results.mappings().all()

@router.get("/conferences/{lab_id}")
async def get_publications(lab_id:int, user:RleSession = Depends(get_session), db:Session = Depends(get_db)):
    sql = text(Path("sql/conference.sql").read_text().format(lab_id))
    results = db.execute(sql)
    return results.mappings().all()


@router.get("/research/{lab_id}")
async def get_publications(lab_id:int, user:RleSession = Depends(get_session), db:Session = Depends(get_db)):
    response = dict()
    upcoming_conference = db.execute(text(Path("sql/research_conference.sql").read_text().format(lab_id))).mappings().all()
    response['upcoming_conference'] = upcoming_conference
    top_5_papers = db.execute(text(Path("sql/research_publication.sql").read_text().format(lab_id))).mappings().all()
    response['top_5_papers'] = top_5_papers
    return response



@router.post("/publication")
async def add_publication(pub: schemas.PublicationAdd ,user:RleSession = Depends(get_session), db:Session = Depends(get_db)):

    CHECK_ACCESS(user, USER_ROLE["manager"])

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
async def add_conference(conf: schemas.ConferenceAdd ,user:RleSession = Depends(get_session), db:Session = Depends(get_db)):

    CHECK_ACCESS(user, USER_ROLE["user"])

    ## Insert into Binary table 
    conference_bin_id = await insert_into_binary_table(db,conf.conf_pdf)

    ## Publication Table entry
    conference_entry = models.Conference(
        conf_title = conf.conf_title,
        conf_binary_id = conference_bin_id,
        description = conf.description,

        start_date = conf.start_date,
        end_date = conf.end_date,

        lab_id = conf.lab_id
        #created_by = 1##TODO: Insert logeed in perosn id
    )

    db.add(conference_entry)
    db.commit()
    db.refresh(conference_entry)

    return conference_entry.id


@router.post("/patent")
async def add_patent(patent: schemas.PatentAdd ,user:RleSession = Depends(get_session), db:Session = Depends(get_db)):
    
    CHECK_ACCESS(user, USER_ROLE["user"])
    
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

## To Update A Conference
@router.put("/conference/{conf_id}")
async def update_conference(conf_id:int,conf: schemas.ConferenceUpdate ,user:RleSession = Depends(get_session), db:Session = Depends(get_db)):
    
    CHECK_ACCESS(user, USER_ROLE["user"])


    db_item = db.query(models.Conference).filter(models.Conference.id==conf_id).first()
    db_blob_storage = db.query(models.Binary).filter(models.Binary.id == db_item.conf_binary_id).first()
    if not db_item:
        return {"error":"Item not found"}
    
    if conf.conf_pdf:
        db_blob_storage.blob_storage = conf.conf_pdf

    update_conference_data = {k: v for k, v in conf.dict(exclude_unset=True).items()}
    for key, value in update_conference_data.items():
        setattr(db_item, key, value)

    db.commit()

    return "Success"

## to delete a conference - Completed
@router.delete("/conference")
async def delete_conference_by_id(conf_id:int,user:RleSession = Depends(get_session), db:Session = Depends(get_db)):

    CHECK_ACCESS(user, USER_ROLE["manager"])

    conference = db.get(models.Conference,conf_id)
    conference_file = db.get(models.Binary,conference.conf_binary_id)
    db.delete(conference)
    db.delete(conference_file)
    db.commit()
    return "" 

## To Update A Publication
@router.put("/publication/{pub_id}")
async def update_publication(pub_id:int,pub: schemas.PublicationUpdate ,user:RleSession = Depends(get_session), db:Session = Depends(get_db)):
    
    CHECK_ACCESS(user, USER_ROLE["user"])


    db_item = db.query(models.Publication).filter(models.Publication.id==pub_id).first()
    db_blob_storage = db.query(models.Binary).filter(models.Binary.id == db_item.pub_binary_id).first()
    if not db_item:
        return {"error":"Item not found"}
    
    if pub.pub_pdf:
        db_blob_storage.blob_storage = pub.pub_pdf

    update_publication_data = {k: v for k, v in pub.dict(exclude_unset=True).items()}
    for key, value in update_publication_data.items():
        setattr(db_item, key, value)

    db.commit()

    return "Success"

## to delete a publication - Completed
@router.delete("/publication")
async def delete_publication_by_id(publication_id:int,user:RleSession = Depends(get_session), db:Session = Depends(get_db)):

    CHECK_ACCESS(user, USER_ROLE["manager"])


    publication = db.get(models.Publication,publication_id)
    publication_file = db.get(models.Binary,publication.pub_binary_id)
    patent_on_publication = db.query(models.Patent).filter(models.Patent.publication_id == publication_id).all()
    for pat in patent_on_publication:
        db.delete(pat)
    db.delete(publication)
    db.delete(publication_file)
    db.commit()
    return ""

## To Update a Patent
@router.put("/patent/{patent_id}")
async def update_patent(patent_id:int,patent: schemas.PatentUpdate ,user:RleSession = Depends(get_session), db:Session = Depends(get_db)):
    
    CHECK_ACCESS(user, USER_ROLE["user"])


    db_item = db.query(models.Patent).filter(models.Patent.id==patent_id).first()
    if not db_item:
        return {"error":"Item not found"}

    update_patent_data = {k: v for k, v in patent.dict(exclude_unset=True).items()}
    for key, value in update_patent_data.items():
        setattr(db_item, key, value)

    db.commit()

    return "Success"

## to delete a patent - Completed
@router.delete("/patent")
async def delete_patent_by_id(patent_id:int,user:RleSession = Depends(get_session), db:Session = Depends(get_db)):

    CHECK_ACCESS(user, USER_ROLE["manager"])


    db.delete(db.get(models.Patent,patent_id))
    db.commit()
    return ""