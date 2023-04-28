from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import models, schemas
from utils import get_db, insert_into_binary_table

router = APIRouter()


## Event creation
@router.post("/event")
async def add_event(event: schemas.EventAdd ,db: Session = Depends(get_db)):
    event_bin_id = await insert_into_binary_table(db,event.event_image)

    ## Event Table entry
    event_entry = models.Events(
        lab_id = event.lab_id,
        title = event.title,
        description = event.description,
        event_date = event.event_date,
        binary_id = event_bin_id,
        is_active = True,
        #created_by = 1##TODO: Insert logeed in perosn id
    )

    db.add(event_entry)
    db.commit()
    db.refresh(event_entry)

    return event_entry.id


## to delete a event
@router.delete("/event")
async def delete_event_by_id(event_id:int,db: Session = Depends(get_db)):
    db.delete(db.get(models.Events,event_id))
    db.commit()
    return ""


## New PosterDemo Creation
@router.post("/posterdemo")
async def add_poster_demo(posdem: schemas.PosterDemoAdd ,db: Session = Depends(get_db)):
    posdem_bin_id = await insert_into_binary_table(db,posdem.poster_demo_image)

    ## Event Table entry
    posdem_entry = models.PosterDemo(
        lab_id = posdem.lab_id,
        description = posdem.description,
        binary_id = posdem_bin_id,
        type = posdem.type,
        is_active = True,
        #created_by = 1##TODO: Insert logeed in perosn id
    )

    db.add(posdem_entry)
    db.commit()
    db.refresh(posdem_entry)

    return posdem_entry.id


## to delete a PosterDemo
@router.delete("/posterdemo")
async def delete_posterdemo_by_id(posdem_id:int,db: Session = Depends(get_db)):
    db.delete(db.get(models.PosterDemo,posdem_id))
    db.commit()
    return "" 