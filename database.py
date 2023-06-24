from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import Base

SQLALCHEMY_DATABASE_URL = "postgresql://shaikmohammedsayeed2:dEjBXls6bHg4@ep-throbbing-heart-402486.us-east-2.aws.neon.tech/test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)