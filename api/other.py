from fastapi import Depends, File, APIRouter,UploadFile
from sqlalchemy.orm import Session
import models, schemas
from azure.storage.blob import BlobServiceClient
from utils import get_db

router = APIRouter()

STORAGE_ACCOUNT_KEY = "sas9P21AXygSyNPuDf7ckmuX4bctEVeKy78IpCfLdGcfh9ROBv2stQ+SGAfL8PffOGGUtZW3VPnI+AStRY3dYg=="
STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=rlestoragefree;AccountKey=sas9P21AXygSyNPuDf7ckmuX4bctEVeKy78IpCfLdGcfh9ROBv2stQ+SGAfL8PffOGGUtZW3VPnI+AStRY3dYg==;EndpointSuffix=core.windows.net"
IMAGE_CONTAINER = "rleassests"


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(IMAGE_CONTAINER)
    blob_client = container_client.get_blob_client(file.filename)
    data = await file.read()
    blob_client.upload_blob(data,overwrite=True)
    return {
        "url":blob_client.url,
        "filename": file.filename
        }


@router.post("/feedback")
async def submit_feedback(feedback: schemas.FeedbackAdd ,db: Session = Depends(get_db)):
    feedback_entry = models.Feedback(
        lab_id = feedback.lab_id,
        name = feedback.name,
        email = feedback.email,
        subject = feedback.subject,
        message = feedback.message
    )

    db.add(feedback_entry)
    db.commit()
    db.refresh(feedback_entry)

    return feedback_entry.id

@router.get("/feedback/{lab_id}")
async def get_all_feedback(lab_id:int, db: Session = Depends(get_db)):
    return db.query(models.Feedback).filter(models.Feedback.lab_id == lab_id).all()

@router.delete("/feedback")
async def delete_all_feedbacks_by_id(feedback_ids:list[int],db: Session = Depends(get_db)):
    for feedid in feedback_ids:
        feedback = db.get(models.Feedback,feedid)
        db.delete(feedback)
    
    db.commit()
    return ""  

@router.delete("/feedback/{lab_id}")
async def delete_all_feedbacks_by_labid(lab_id:int,db: Session = Depends(get_db)):
    db_feedbacks = db.query(models.Feedback).filter(models.Feedback.lab_id == lab_id).all()  
    db.delete(db_feedbacks)
    return ""