from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy import text
from pathlib import Path
from utils import *
from session import RleSession

router = APIRouter()


@router.get("/labs", response_model=list[schemas.Lab])
async def read_users(user:RleSession = Depends(get_session), db:Session = Depends(get_db)):
    labs = db.query(models.Lab).all()
    print(labs)
    return labs

@router.get("/home/{lab_id}")
async def get_home_details(lab_id:int, user:RleSession = Depends(get_session), db:Session = Depends(get_db)):
    lab = db.get(models.Lab, lab_id)
    # assert type(lab)==models.Lab
    response = dict()
    # Event details
    response["name"] = lab.name
    response["logo"] = db.get(models.Binary, lab.lab_logo_id).blob_storage
    response["cover_url"] = db.get(models.Binary, lab.cover_binary_id)
    response['contact_us'] =  lab._contact_us
    response['twitter_handle'] = lab.twitter_handle
    response['overview'] = lab.overview
    response['events'] = await get_home_events(lab_id, db)
    # Slider handle
    slider = db.execute(text(Path("sql/slider.sql").read_text().format(lab_id))).mappings().all()
    response['slider'] = slider
    # News handle
    news = db.execute(text(Path("sql/news.sql").read_text().format(lab_id))).mappings().all()
    response['news'] = news
    ## Counts
    response["metrics"] = await get_resarch_metrics(lab_id,db)
    return response





async def get_resarch_metrics(lab_id:int, db: Session):
    # Conference table contains other conference (Local, etc..)
    # Publication table contains internaational Confernces and Journals
    confenceCount = db.query(models.Publication).filter(models.Publication.type == "conference",models.Publication.lab_id == lab_id).count()
    return {
        "patentCount":      db.query(models.Patent).filter(models.Patent.lab_id == lab_id).count(),
        "posterDemoCount":  db.query(models.PosterDemo).filter(models.PosterDemo.lab_id == lab_id).count(),
        "conferencesCount": confenceCount + db.query(models.Conference).filter(models.Conference.lab_id == lab_id).count(),
        "journalCount":     db.query(models.Publication).filter(models.Publication.type == "journal",models.Publication.lab_id == lab_id).count()
            }



async def get_home_events(lab_id:int, db:Session):
    sql = text(Path("sql/home_events.sql").read_text().format(lab_id))
    results = db.execute(sql)
    return results.mappings().all()