from pathlib import Path

from fastapi import Depends, APIRouter
from sqlalchemy import text

import schemas
from utils import *

router = APIRouter()


## Get All Events
@router.get("/event/{lab_id}")
async def get_all_events(lab_id: int, user: RleSession = Depends(get_session), db: Session = Depends(get_db)):
    sql = text(Path("sql/all_events.sql").read_text().format(lab_id))
    results = db.execute(sql)
    return results.mappings().all()


## Event creation
@router.post("/event")
async def add_event(event: schemas.EventAdd, user: RleSession = Depends(get_session), db: Session = Depends(get_db)):
    CHECK_ACCESS(user, USER_ROLE["user"])

    # Manager and User should be of same lab
    if user.role_id != USER_ROLE["admin"] and user.lab_id != event.lab_id: 
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    event_bin_id = await insert_into_binary_table(db, event.event_image)

    ## Event Table entry
    event_entry = models.Events(
        lab_id=event.lab_id,
        title=event.title,
        description=event.description,
        event_date=event.event_date,
        binary_id=event_bin_id,
        is_active=True,
        # created_by = 1##TODO: Insert logeed in perosn id
    )

    db.add(event_entry)
    db.commit()
    db.refresh(event_entry)

    return event_entry.id


## New Event Creation Api Along with gallery
@router.post("/newevent")
async def add_new_event(event: schemas.NewEventAdd, user: RleSession = Depends(get_session),
                        db: Session = Depends(get_db)):
    CHECK_ACCESS(user, USER_ROLE["manager"])

    # Manager and User should be of same lab
    if user.role_id != USER_ROLE["admin"] and user.lab_id != event.lab_id: 
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    event_bin_id = await insert_into_binary_table(db, event.event_image)

    event_entry = models.Events(
        lab_id=event.lab_id,
        title=event.title,
        description=event.description,
        event_date=event.event_date,
        binary_id=event_bin_id,
        is_active=True
    )

    db.add(event_entry)
    db.commit()
    db.refresh(event_entry)

    created_event_id = event_entry.id

    for image in event.gallery_images_url:
        gallery_bin_id = await insert_into_binary_table(db, image)

        gallery_entry = models.Gallery(
            event_id=created_event_id,
            binary_id=gallery_bin_id
        )

        db.add(gallery_entry)

    db.commit()

    return created_event_id


## To Update A Event
@router.put("/event/{event_id}")
async def update_event(event_id: int, event: schemas.EventUpdate, user: RleSession = Depends(get_session),
                       db: Session = Depends(get_db)):
    CHECK_ACCESS(user, USER_ROLE["user"])

    db_item = db.query(models.Events).filter(models.Events.id == event_id).first()
    db_blob_storage = db.query(models.Binary).filter(models.Binary.id == db_item.binary_id).first()
    if not db_item:
        return {"error": "Item not found"}
    
    # Manager and User should be of same lab
    if user.role_id != USER_ROLE["admin"] and user.lab_id != db_item.lab_id: 
        raise HTTPException(status_code=401, detail="Unauthorized")

    if event.event_image:
        db_blob_storage.blob_storage = event.event_image

    update_event_data = {k: v for k, v in event.dict(exclude_unset=True).items()}
    for key, value in update_event_data.items():
        setattr(db_item, key, value)

    db.commit()

    return "Success"


## to delete a event - Completed
@router.delete("/event")
async def delete_event_by_id(event_id: int, user: RleSession = Depends(get_session), db: Session = Depends(get_db)):
    CHECK_ACCESS(user, USER_ROLE["manager"])

    event = db.get(models.Events, event_id)

    # Manager and User should be of same lab
    if user.role_id != USER_ROLE["admin"] and user.lab_id != event.lab_id: 
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    event_cover_image = db.get(models.Binary, event.binary_id)
    db.delete(event)
    db.commit()
    db.delete(event_cover_image)
    db.commit()
    return ""


## New PosterDemo Creation
@router.post("/posterdemo")
async def add_poster_demo(posdem: schemas.PosterDemoAdd, user: RleSession = Depends(get_session),
                          db: Session = Depends(get_db)):
    CHECK_ACCESS(user, USER_ROLE["user"])

    # Manager and User should be of same lab
    if user.role_id != USER_ROLE["admin"] and user.lab_id != posdem.lab_id: 
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    posdem_bin_id = await insert_into_binary_table(db, posdem.poster_demo_image)

    ## Event Table entry
    posdem_entry = models.PosterDemo(
        lab_id=posdem.lab_id,
        description=posdem.description,
        binary_id=posdem_bin_id,
        type=posdem.type,
        is_active=True,
        # created_by = 1##TODO: Insert logeed in perosn id
    )

    db.add(posdem_entry)
    db.commit()
    db.refresh(posdem_entry)

    return posdem_entry.id


@router.delete("/posterdemo")
async def delete_posterdemo_by_id(posdem_id: int, user: RleSession = Depends(get_session),
                                  db: Session = Depends(get_db)):
    CHECK_ACCESS(user, USER_ROLE["manager"])
    
    poster = db.get(models.PosterDemo, posdem_id)
    # Manager and User should be of same lab
    if user.role_id != USER_ROLE["admin"] and user.lab_id != poster.lab_id: 
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    poster_binary = db.get(models.Binary, poster.binary_id)
    db.delete(poster)
    db.commit()
    db.delete(poster_binary)
    db.commit()
    return ""


## To Update A Poster or Demo
@router.put("/posterdemo/{posterdemo_id}")
async def update_poster(posterdemo_id: int, posdem: schemas.PosterDemoUpdate, user: RleSession = Depends(get_session),
                        db: Session = Depends(get_db)):
    CHECK_ACCESS(user, USER_ROLE["user"])
    
    db_item = db.query(models.PosterDemo).filter(models.PosterDemo.id == posterdemo_id).first()
    db_blob_storage = db.query(models.Binary).filter(models.Binary.id == db_item.binary_id).first()
    if not db_item:
        return {"error": "Item not found"}

    # Manager and User should be of same lab
    if user.role_id != USER_ROLE["admin"] and user.lab_id != db_item.lab_id: 
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if posdem.poster_demo_image:
        db_blob_storage.blob_storage = posdem.poster_demo_image

    update_posterdemo_data = {k: v for k, v in posdem.dict(exclude_unset=True).items()}
    for key, value in update_posterdemo_data.items():
        setattr(db_item, key, value)

    db.commit()

    return "Success"
