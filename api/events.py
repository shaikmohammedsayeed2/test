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

## To Update A Event
@router.put("/event/{event_id}")
async def update_event(event_id:int,event: schemas.EventUpdate ,db: Session=Depends(get_db)):
    
    db_item = db.query(models.Events).filter(models.Events.id==event_id).first()
    db_blob_storage = db.query(models.Binary).filter(models.Binary.id == db_item.binary_id).first()
    if not db_item:
        return {"error":"Item not found"}
    
    if event.event_image:
        db_blob_storage.blob_storage = event.event_image

    update_event_data = {k: v for k, v in event.dict(exclude_unset=True).items()}
    for key, value in update_event_data.items():
        setattr(db_item, key, value)

    db.commit()

    return "Success" 

## to delete a event - Completed
@router.delete("/event")
async def delete_event_by_id(event_id:int,db: Session = Depends(get_db)):
    event = db.get(models.Events,event_id)
    event_cover_image = db.get(models.Binary,event.binary_id)
    db.delete(event)
    db.delete(event_cover_image)
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


@router.delete("/posterdemo")
async def delete_posterdemo_by_id(posdem_id:int,db: Session = Depends(get_db)):
    poster = db.get(models.PosterDemo,posdem_id)
    poster_binary = db.get(models.Binary,poster.binary_id)
    db.delete(poster)
    db.delete(poster_binary)
    db.commit()
    return "" 

## To Update A Poster or Demo
@router.put("/posterdemo/{posterdemo_id}")
async def update_poster(posterdemo_id:int,posdem: schemas.PosterDemoUpdate ,db: Session=Depends(get_db)):
    
    db_item = db.query(models.PosterDemo).filter(models.PosterDemo.id==posterdemo_id).first()
    db_blob_storage = db.query(models.Binary).filter(models.Binary.id == db_item.binary_id).first()
    if not db_item:
        return {"error":"Item not found"}
    
    if posdem.poster_demo_image:
        db_blob_storage.blob_storage = posdem.poster_demo_image

    update_posterdemo_data = {k: v for k, v in posdem.dict(exclude_unset=True).items()}
    for key, value in update_posterdemo_data.items():
        setattr(db_item, key, value)

    db.commit()

    return "Success"