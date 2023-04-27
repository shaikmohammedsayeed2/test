from pydantic import BaseModel

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
    # Binaries
    pub_pdf:str

class ConferenceAdd(BaseModel):
    conf_title: str
    description: str
    lab_id: int
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
    gallery_image: str