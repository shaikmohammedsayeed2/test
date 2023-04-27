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