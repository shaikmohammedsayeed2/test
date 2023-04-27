from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
from fastapi.middleware.cors import CORSMiddleware
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient
from sqlalchemy import select,text
from pathlib import Path

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

@app.get("/research/{lab_id}")
async def get_resarch_counts(lab_id:int, db: Session = Depends(get_db)):
    # Conference table contains other conference (Local, etc..)
    # Publication table contains internaational Confernces and Journals
    confenceCount = db.query(models.Publication).filter(models.Publication.type == "conference",models.Publication.lab_id == lab_id).count()
    return {
        "patentCount":      db.query(models.Patent).filter(models.Patent.lab_id == lab_id).count(),
        "posterDemoCount":  db.query(models.PosterDemo).filter(models.PosterDemo.lab_id == lab_id).count(),
        "conferencesCount": confenceCount + db.query(models.Conference).filter(models.Conference.lab_id == lab_id).count(),
        "journalCount":     db.query(models.Publication).filter(models.Publication.type == "journal",models.Publication.lab_id == lab_id).count()
            }


@app.get("/home/{lab_id}")
async def get_home_details(lab_id:int, db: Session = Depends(get_db)):
    lab = db.get(models.Lab, lab_id)
    assert type(lab)==models.Lab
    response = dict()
    # Event details
    response["Name"] = lab.name
    response["logo"] = db.get(models.Binary, lab.lab_logo_id).blob_storage
    response['ContactUs'] =  lab._contact_us
    response['TwitterHandle'] = lab.twitter_handle
    response['Overview'] = lab.overview
    response['Events'] = lab._events
    # Slider handle
    slider = db.execute(text(Path("sql/slider.sql").read_text().format(lab_id))).mappings().all()
    response['slider'] = slider
    
    return response

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