from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy import text
from pathlib import Path
from utils import get_db, insert_into_binary_table

router = APIRouter()

@router.get("/gallery/{lab_id}")
async def get_gallery(lab_id:int, db: Session = Depends(get_db)):
    sql = text(Path("sql/gallery.sql").read_text().format(lab_id))
    results = db.execute(sql)
    return results.mappings().all()




   
## New Gallery Image Creation
@router.post("/galleryimage")
async def add_gallery_image(gallery: schemas.GalleryImageAdd ,db: Session = Depends(get_db)):
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

## to delete images from gallery
@router.delete("/images")
async def delete_images_by_id(imageids:list[int],db: Session = Depends(get_db)) :
    for imageid in imageids:
        db.delete(db.get(models.Gallery,imageid))
    db.commit()  
    return ""

#########################################################

@router.post("/sliderimage")
async def add_slider_image(sli: schemas.SliderImageAdd ,db: Session = Depends(get_db)):
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


## to delete a slider image
@router.delete("/slider")
async def delete_slider_image_by_id(slider_id:int,db: Session = Depends(get_db)):
    db.delete(db.get(models.Slider,slider_id))
    db.commit()
    return ""