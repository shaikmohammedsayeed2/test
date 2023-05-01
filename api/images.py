from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy import text
from pathlib import Path
from utils import *
from session import RleSession

router = APIRouter()

@router.get("/gallery/{lab_id}")
async def get_gallery(lab_id:int, user:RleSession = Depends(get_session), db:Session = Depends(get_db)):
    sql = text(Path("sql/gallery.sql").read_text().format(lab_id))
    results = db.execute(sql)
    return results.mappings().all()




   
## New Gallery Image Creation
@router.post("/galleryimage")
async def add_gallery_image(gallery: schemas.GalleryImageAdd ,user:RleSession = Depends(get_session), db:Session = Depends(get_db)):
    
    CHECK_ACCESS(user, USER_ROLE["manager"])


    for image in gallery.gallery_images_url:
        gallery_bin_id = await insert_into_binary_table(db,image)

        ## Gallery Table entry
        gallery_entry = models.Gallery(
            event_id = gallery.event_id,
            binary_id = gallery_bin_id,
            #is_active = True,
            #created_by = 1##TODO: Insert logeed in perosn id
        )

        db.add(gallery_entry)
    
    db.commit()
    return 

## to delete images from gallery - Completed
@router.delete("/images")
async def delete_images_by_id(imageids:list[int],user:RleSession = Depends(get_session), db:Session = Depends(get_db)) :
    
    CHECK_ACCESS(user, USER_ROLE["manager"])

    for imageid in imageids:
        image = db.get(models.Gallery,imageid)
        image_binary = db.get(models.Binary,image.binary_id)
        db.delete(image)
        db.delete(image_binary)
    db.commit()  
    return ""

#########################################################

@router.post("/sliderimage")
async def add_slider_image(sli: schemas.SliderImageAdd ,user:RleSession = Depends(get_session), db:Session = Depends(get_db)):
    
    CHECK_ACCESS(user, USER_ROLE["manager"])

    
    sli_bin_id = await insert_into_binary_table(db,sli.slider_image)

    ## Slider Table entry
    sli_entry = models.Slider(
        lab_id = sli.lab_id,
        slider_binary_id = sli_bin_id,
        is_active = True,
        #created_by = 1##TODO: Insert logeed in perosn id
    )

    db.add(sli_entry)
    db.commit()
    db.refresh(sli_entry)

    return sli_entry.id

## To Update A Slider Image
@router.put("/sliderimage/{slider_id}")
async def update_slider_image(slider_id:int,slider: schemas.SliderImageUpdate ,user:RleSession = Depends(get_session), db:Session = Depends(get_db)):
    
    CHECK_ACCESS(user, USER_ROLE["manager"])


    db_item = db.query(models.Slider).filter(models.Slider.id==slider_id).first()
    db_blob_storage = db.query(models.Binary).filter(models.Binary.id == db_item.slider_binary_id).first()
    if not db_item:
        return {"error":"Item not found"}
    
    if slider.slider_image:
        db_blob_storage.blob_storage = slider.slider_image

    update_slider_data = {k: v for k, v in slider.dict(exclude_unset=True).items()}
    for key, value in update_slider_data.items():
        setattr(db_item, key, value)

    db.commit()

    return "Success"

## to delete a slider image
@router.delete("/slider")
async def delete_slider_image_by_id(slider_id:int,user:RleSession = Depends(get_session), db:Session = Depends(get_db)):
    
    CHECK_ACCESS(user, USER_ROLE["manager"])

    
    slider_image = db.get(models.Slider,slider_id)
    slider_image_binary = db.get(models.Binary,slider_image.slider_binary_id)
    db.delete(slider_image)
    db.delete(slider_image_binary)
    db.commit()
    return ""