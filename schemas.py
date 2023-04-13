from pydantic import BaseModel

class Lab(BaseModel):
    id :int
    name: str
    overview: str

    class Config:
        orm_mode = True
