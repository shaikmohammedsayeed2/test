from pydantic import BaseModel
import datetime
from typing import Optional


class Lab(BaseModel):
    id :int
    name: str
    overview: str

    class Config:
        orm_mode = True

class LabAdd(BaseModel):
    name: str
    overview: str
    address: str
    email: str
    phone: str
    twitter_handle:str
    # Binaries
    lab_logo_url :str
    lab_cover_url: str

class PublicationAdd(BaseModel):
    pub_title: str
    description: str
    lab_id: int
    type: str
    pub_date : datetime.date
    # Binaries
    pub_pdf:str

class ConferenceAdd(BaseModel):
    conf_title: str
    description: str
    lab_id: int
    start_date : datetime.date
    end_date   : datetime.date
    # Binaries
    conf_pdf:str

class ContactUsAdd(BaseModel):
    address: str
    email: str
    phone: str

class PersonAdd(BaseModel):
    name: str
    roll_number: str
    linkedin_url: str
    github_url: str
    personal_web_url: str
    # Role
    lab_id: int
    person_role: str
    user_role: str
    # Binaries
    person_image: str

class PatentAdd(BaseModel):
    publication_id:int
    description:str
    lab_id:int

class EventAdd(BaseModel):
    lab_id: int
    title: str
    description: str
    event_date : datetime.date
    # Binaries
    event_image: str

class PosterDemoAdd(BaseModel):
    lab_id: int
    description: str
    type:str
    # Binaries
    poster_demo_image: str

class SliderImageAdd(BaseModel):
    lab_id: int
    # Binaries
    slider_image: str

class GalleryImageAdd(BaseModel):
    event_id: int
    # Binaries
    gallery_images_url: list[str]


class FeedbackAdd(BaseModel):
    lab_id:int
    name:str 
    email:str
    subject: str
    message: str

class LabUpdate(BaseModel):
    name: Optional[str]
    overview: Optional[str]
    address: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    twitter_handle:Optional[str]
    # Binaries
    lab_logo_url :Optional[str]
    lab_cover_url: Optional[str]

class PublicationUpdate(BaseModel):
    pub_title: Optional[str]
    description: Optional[str]
    lab_id: Optional[int]
    type: Optional[str]
    pub_date : Optional[datetime.date]
    # Binaries
    pub_pdf:Optional[str] 

class ConferenceUpdate(BaseModel):
    conf_title: Optional[str]
    description: Optional[str]
    lab_id: Optional[int]
    start_date : Optional[datetime.date]
    end_date   : Optional[datetime.date]
    # Binaries
    conf_pdf:Optional[str]   

class PatentUpdate(BaseModel):
    publication_id:Optional[int]
    description:Optional[str]
    lab_id:Optional[int] 

class EventUpdate(BaseModel):
    lab_id: Optional[int]
    title: Optional[str]
    description: Optional[str]
    event_date :Optional[datetime.date]
    # Binaries
    event_image: Optional[str] 

class PosterDemoUpdate(BaseModel):
    lab_id:Optional[int]
    description: Optional[str]
    type:Optional[str]
    # Binaries
    poster_demo_image: Optional[str]  
    
class SliderImageUpdate(BaseModel):
    lab_id: Optional[int]
    # Binaries
    slider_image: Optional[str] 

## Unable to edit Galeery since it will change all the images  

class PersonUpdate(BaseModel):
    name: Optional[str]
    roll_number: Optional[str]
    linkedin_url: Optional[str]
    github_url: Optional[str]
    personal_web_url: Optional[str]
    # Role
    lab_id: Optional[int]
    person_role: Optional[str]
    user_role: Optional[str]
    # Binaries
    person_image: Optional[str]               