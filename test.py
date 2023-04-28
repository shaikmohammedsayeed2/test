from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
from fastapi.middleware.cors import CORSMiddleware
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient
from sqlalchemy import select,text
from pathlib import Path
from fastapi.responses import RedirectResponse

STORAGE_ACCOUNT_KEY = "sas9P21AXygSyNPuDf7ckmuX4bctEVeKy78IpCfLdGcfh9ROBv2stQ+SGAfL8PffOGGUtZW3VPnI+AStRY3dYg=="
STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=rlestoragefree;AccountKey=sas9P21AXygSyNPuDf7ckmuX4bctEVeKy78IpCfLdGcfh9ROBv2stQ+SGAfL8PffOGGUtZW3VPnI+AStRY3dYg==;EndpointSuffix=core.windows.net"
IMAGE_CONTAINER = "rleassests"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

###############################################
# from enum import Enum

# class USER_ROLE(Enum):
#     admin = 1
#     user = 2
#     manager = 3

# class PERSON_ROLE(Enum):
#     student = 1
#     faculty = 2
#     staff = 3

PERSON_ROLE = {"student" : 1,"faculty" : 2,"staff" : 3,"sponsor":4}
USER_ROLE = {"admin":1,"user":2,"manager":3}

###############################################

@app.get("/")
def redirect():
    return RedirectResponse("/docs")

@app.get("/labs", response_model=list[schemas.Lab])
async def read_users(db: Session = Depends(get_db)):
    labs = db.query(models.Lab).all()
    print(labs)
    return labs


## Function to get the members of the given lab
@app.get("/people/{lab_id}")
async def get_people(lab_id:int, db: Session = Depends(get_db)):
    sql = text(Path("sql/people.sql").read_text().format(lab_id))
    results = db.execute(sql)
    return results.mappings().all()


@app.get("/gallery/{lab_id}")
async def get_gallery(lab_id:int, db: Session = Depends(get_db)):
    sql = text(Path("sql/gallery.sql").read_text().format(lab_id))
    results = db.execute(sql)
    return results.mappings().all()

#############################################################
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

async def get_home_events(lab_id:int, db: Session = Depends(get_db)):
    sql = text(Path("sql/home_events.sql").read_text().format(lab_id))
    results = db.execute(sql)
    return results.mappings().all()

@app.get("/home/{lab_id}")
async def get_home_details(lab_id:int, db: Session = Depends(get_db)):
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
    ## Counts
    response["metrics"] = await get_resarch_metrics(lab_id,db)
    return response


#############################################################

@app.get("/publications/{lab_id}")
async def get_publications(lab_id:int, db: Session = Depends(get_db)):
    sql = text(Path("sql/publications.sql").read_text().format(lab_id))
    results = db.execute(sql)
    return results.mappings().all()

@app.get("/conferences/{lab_id}")
async def get_publications(lab_id:int, db: Session = Depends(get_db)):
    sql = text(Path("sql/conference.sql").read_text().format(lab_id))
    results = db.execute(sql)
    return results.mappings().all()


@app.get("/research/{lab_id}")
async def get_publications(lab_id:int, db: Session = Depends(get_db)):
    sql = text(Path("sql/conference.sql").read_text().format(lab_id))
    results = db.execute(sql)
    return results.mappings().all()

############################################################################################

###                              POST REQUESTS                                          ###

############################################################################################




@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(IMAGE_CONTAINER)
    blob_client = container_client.get_blob_client(file.filename)
    data = await file.read()
    blob_client.upload_blob(data)
    return {
        "url":blob_client.url,
        "filename": file.filename
        }


@app.post("/feedback")
async def submit_feedback(feedback: schemas.FeedbackAdd ,db: Session = Depends(get_db)):
    feedback_entry = models.Feedback(
        name = feedback.name,
        email = feedback.email,
        subject = feedback.subject,
        message = feedback.message
    )

    db.add(feedback_entry)
    db.commit()
    db.refresh(feedback_entry)

    return feedback_entry.id




#################################################

async def insert_into_binary_table(db:Session, url:str):
    bin_entry = models.Binary(
        blob_storage = url,
        is_active = True,
        # blob_size = -1,
        #created_by = 1      ##TODO: Insert logeed in perosn id
    )
    db.add(bin_entry)
    db.commit()
    db.refresh(bin_entry)

    return bin_entry.id
    

## New lab creation
async def create_lab(lab: schemas.LabAdd ,db: Session):
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


    


@app.post("/lab")
async def add_lab(lab: schemas.LabAdd ,db: Session = Depends(get_db)):
    return await create_lab(lab,db)

############################################################################

## New Publication Creation

async def create_publication(pub: schemas.PublicationAdd ,db: Session):
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


@app.post("/publication")
async def add_publication(pub: schemas.PublicationAdd ,db: Session = Depends(get_db)):
    return await create_publication(pub,db)

########################################################################################################################
## New Conference Creation

async def create_conference(conf: schemas.ConferenceAdd ,db: Session):
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
        is_active = True,
        #created_by = 1##TODO: Insert logeed in perosn id
    )

    db.add(conference_entry)
    db.commit()
    db.refresh(conference_entry)

    return conference_entry.id


@app.post("/conference")
async def add_conference(conf: schemas.ConferenceAdd ,db: Session = Depends(get_db)):
    return await create_conference(conf,db)  

##############################################################################################################

## New ContactUs Creation

async def create_contactus(contact: schemas.ContactUsAdd ,db: Session):

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


@app.post("/contactus")
async def add_contactus(contact: schemas.ContactUsAdd ,db: Session = Depends(get_db)):
    return await create_contactus(contact,db) 

#######################################################################################################################

## New Person Creation

async def create_person(person: schemas.PersonAdd ,db: Session):

    # Checks 
    try:
        assert person.person_role.lower() in PERSON_ROLE.keys() 
        assert person.user_role.lower() in USER_ROLE.keys() 
    except AssertionError:
        raise HTTPException(status_code=422, detail="Person role argument invalid")
    
    

    person_bin_id = await insert_into_binary_table(db,person.person_image)

    ## Person Table entry
    person_entry = models.Person(
        name = person.name,
        roll_number = person.roll_number,
        linkedin_url = person.linkedin_url,
        github_url = person.github_url,
        personal_web_url = person.personal_web_url,
        profile_binary_id = person_bin_id,
        is_active = True,
        #created_by = 1##TODO: Insert logeed in perosn id
    )

    db.add(person_entry)
    db.commit()
    db.refresh(person_entry)

    

    ## Lab Member table entry
    lab_mem_entry = models.LabMember(
        person_id = person_entry.id,
        lab_id= person.lab_id,
        role_id = USER_ROLE[person.user_role],
        person_role_id = PERSON_ROLE[person.person_role]

    )

    db.add(lab_mem_entry)
    db.commit()
    db.refresh(lab_mem_entry)

    return person_entry.id


@app.post("/person")
async def add_person(person: schemas.PersonAdd ,db: Session = Depends(get_db)):
    return await create_person(person,db) 

#######################################################################################################

## New Patent Creation

async def create_patent(patent: schemas.PatentAdd ,db: Session):

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


@app.post("/patent")
async def add_patent(patent: schemas.PatentAdd ,db: Session = Depends(get_db)):
    return await create_patent(patent,db)

###########################################################################################################

## New Event Creation

async def create_event(event: schemas.EventAdd ,db: Session):

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


@app.post("/event")
async def add_event(event: schemas.EventAdd ,db: Session = Depends(get_db)):
    return await create_event(event,db)

##################################################################################################################

## New PosterDemo Creation

async def create_poster_demo(posdem: schemas.PosterDemoAdd ,db: Session):

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


@app.post("/posterdemo")
async def add_poster_demo(posdem: schemas.PosterDemoAdd ,db: Session = Depends(get_db)):
    return await create_poster_demo(posdem,db)
 
#########################################################################################################################

## New Slider Image Creation

async def create_slider_image(sli: schemas.SliderImageAdd ,db: Session):

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


@app.post("/sliderimage")
async def add_slider_image(sli: schemas.SliderImageAdd ,db: Session = Depends(get_db)):
    return await create_slider_image(sli,db)

###############################################################################################################################

## New Gallery Image Creation

async def create_gallery_image(gallery: schemas.GalleryImageAdd ,db: Session):

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


@app.post("/galleryimage")
async def add_gallery_image(gallery: schemas.GalleryImageAdd ,db: Session = Depends(get_db)):
    return await create_gallery_image(gallery,db)


#####################################################
## to delete images from gallery - Completed
@app.delete("/images")
async def delete_images_by_id(imageids:list[int],db: Session = Depends(get_db)) :
    for imageid in imageids:
        image = db.get(models.Gallery,imageid)
        image_binary = db.get(models.Binary,image.binary_id)
        db.delete(image)
        db.delete(image_binary)
    db.commit()  
    return ""
####################################################
## to delete a lab - Completed
@app.delete("/lab")
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
####################################################
## to delete a conference - Completed
@app.delete("/conference")
async def delete_conference_by_id(conf_id:int,db: Session = Depends(get_db)):
    conference = db.get(models.Conference,conf_id)
    conference_file = db.get(models.Binary,conference.conf_binary_id)
    db.delete(conference)
    db.delete(conference_file)
    db.commit()
    return "" 
######################################################
## to delete a publication - Completed
@app.delete("/publication")
async def delete_publication_by_id(publication_id:int,db: Session = Depends(get_db)):
    publication = db.get(models.Publication,publication_id)
    publication_file = db.get(models.Binary,publication.pub_binary_id)
    db.delete(publication)
    db.delete(publication_file)
    db.commit()
    return ""
########################################################
## to delete a event - Completed
@app.delete("/event")
async def delete_event_by_id(event_id:int,db: Session = Depends(get_db)):
    event = db.get(models.Events,event_id)
    event_cover_image = db.get(models.Binary,event.binary_id)
    db.delete(event)
    db.delete(event_cover_image)
    db.commit()
    return ""
########################################################
## to delete a patent - Completed
@app.delete("/patent")
async def delete_patent_by_id(patent_id:int,db: Session = Depends(get_db)):
    db.delete(db.get(models.Patent,patent_id))
    db.commit()
    return ""
########################################################
## to delete a PosterDemo - Completed
@app.delete("/posterdemo")
async def delete_posterdemo_by_id(posdem_id:int,db: Session = Depends(get_db)):
    poster = db.get(models.PosterDemo,posdem_id)
    poster_binary = db.get(models.Binary,poster.binary_id)
    db.delete(poster)
    db.delete(poster_binary)
    db.commit()
    return "" 
########################################################
## to delete a slider image
@app.delete("/slider")
async def delete_slider_image_by_id(slider_id:int,db: Session = Depends(get_db)):
    slider_image = db.get(models.Slider,slider_id)
    slider_image_binary = db.get(models.Binary,slider_image.slider_binary_id)
    db.delete(slider_image)
    db.delete(slider_image_binary)
    db.commit()
    return ""
#######################################################
## to delete a person
@app.delete("/labmember")
async def delete_labmember_by_id(labmember_id:int,db: Session = Depends(get_db)):
    person_id = db.get(models.LabMember,labmember_id).person_id
    ref_count = db.query(models.Person).filter(models.Person.id==person_id).count()
    if ref_count == 1:
        db.delete(db.get(models.Person,person_id))
    else:
        db.delete(db.get(models.LabMember,labmember_id))
    db.commit()
    return ""  


#####################################################################################
# ########################## Update Api's ################################################
# #############################################################################

## To Update A Lab
@app.put("/lab/{lab_id}")
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

###########################################################################################
         
## To Update A Publication
@app.put("/publication/{pub_id}")
async def update_publication(pub_id:int,pub: schemas.PublicationUpdate ,db: Session=Depends(get_db)):
    
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

######################################################################################################

## To Update A Conference
@app.put("/conference/{conf_id}")
async def update_conference(conf_id:int,conf: schemas.ConferenceUpdate ,db: Session=Depends(get_db)):
    
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

###########################################################################################################

## To Update a Patent
@app.put("/patent/{patent_id}")
async def update_patent(patent_id:int,patent: schemas.PatentUpdate ,db: Session=Depends(get_db)):
    
    db_item = db.query(models.Patent).filter(models.Patent.id==patent_id).first()
    if not db_item:
        return {"error":"Item not found"}

    update_patent_data = {k: v for k, v in patent.dict(exclude_unset=True).items()}
    for key, value in update_patent_data.items():
        setattr(db_item, key, value)

    db.commit()

    return "Success"

##########################################################################################################

## To Update A Event
@app.put("/event/{event_id}")
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

##############################################################################################################
## To Update A Poster or Demo
@app.put("/posterdemo/{posterdemo_id}")
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

##################################################################################################################
## To Update A Slider Image
@app.put("/sliderimage/{slider_id}")
async def update_slider_image(slider_id:int,slider: schemas.SliderImageUpdate ,db: Session=Depends(get_db)):
    
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

#####################################################################################################################
