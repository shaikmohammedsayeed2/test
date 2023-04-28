from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship
import datetime
from database import Base


class Binary(Base):
    id = Column(Integer, primary_key=True, index=True)

    blob_storage = Column(String)
    # blob_size = Column(Integer)
    is_active = Column(Boolean)
    #created_by = Column(Integer, ForeignKey("TBL_PERSON.id")) 
    created_at = Column(DateTime(timezone=False), default=datetime.datetime.utcnow)

    __tablename__ = 'TBL_BINARY'


class Conference(Base):
    id = Column(Integer, primary_key=True, index=True)

    conf_title = Column(String)
    description = Column(String)
    conf_binary_id = Column(Integer, ForeignKey("TBL_BINARY.id"))
    lab_id = Column(Integer, ForeignKey("TBL_LAB.id"))

    start_date = Column(Date)
    end_date = Column(Date)

    is_active = Column(Boolean)
    #created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))
    created_at = Column(DateTime(timezone=False), default=datetime.datetime.utcnow)

    __tablename__ = 'TBL_CONFERENCE'


class ContactUs(Base):
    id = Column(Integer, primary_key=True, index=True)

    address = Column(String)
    email = Column(String)
    phone = Column(String)
    is_active = Column(Boolean)
    #created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))
    created_at = Column(DateTime(timezone=False), default=datetime.datetime.utcnow)

    __tablename__ = 'TBL_CONTACT_US'


class Lab(Base):
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    lab_logo_id = Column(Integer, ForeignKey("TBL_BINARY.id"))
    cover_binary_id = Column(Integer, ForeignKey("TBL_BINARY.id"))
    overview = Column(String)
    contact_id = Column(Integer, ForeignKey("TBL_CONTACT_US.id"))
    is_active = Column(Boolean)
    #created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))
    created_at = Column(DateTime(timezone=False), default=datetime.datetime.utcnow)
    twitter_handle = Column(String)

    ## Relation
    # _lab_members = relationship("LabMember")
    _lab_members = relationship("LabMember")
    

    # _patents = relationship("Patents")
    # _conference = relationship("Conference")
    # _posterDemo = relationship("PosterDemo")
    # _publications = relationship("Publication")


    _contact_us = relationship("ContactUs") 
    _events = relationship("Events")

    __tablename__ = 'TBL_LAB'


class LabMember(Base):
    id = Column(Integer, primary_key=True, index=True)

    person_id = Column(Integer, ForeignKey("TBL_PERSON.id"))
    lab_id = Column(Integer, ForeignKey("TBL_LAB.id"))
    role_id = Column(Integer, ForeignKey("TBL_ROLE.id"))
    person_role_id = Column(Integer, ForeignKey("TBL_PERSON_ROLE.id"))

    ## Relationship
    _person = relationship("Person")
    __tablename__ = 'TBL_LAB_MEMBER'


class Person(Base):
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    roll_number = Column(String)
    linkedin_url = Column(String)
    github_url = Column(String)
    personal_web_url = Column(String)
    is_active = Column(Boolean)
    created_at = Column(DateTime(timezone=False), default=datetime.datetime.utcnow)
    profile_binary_id = Column(Integer, ForeignKey("TBL_BINARY.id"))
    #created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))


    __tablename__ = 'TBL_PERSON'


class PersonRole(Base):
    id = Column(Integer, primary_key=True, index=True)

    person_role_name = Column(String)  # This field type is a guess.
    is_active = Column(Boolean)

    __tablename__ = 'TBL_PERSON_ROLE'


class Publication(Base):
    id = Column(Integer, primary_key=True, index=True)

    pub_title = Column(String)
    description = Column(String)
    pub_binary_id = Column(Integer, ForeignKey("TBL_BINARY.id"))
    lab_id = Column(Integer, ForeignKey("TBL_LAB.id"))

    pub_date = Column(Date)

    #created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))
    created_at = Column(DateTime(timezone=False), default=datetime.datetime.utcnow)
    type = Column(String)

    __tablename__ = 'TBL_PUBLICATION'


class Role(Base):
    id = Column(Integer, primary_key=True, index=True)

    role_name = Column(String)  
    is_active = Column(Boolean)

    __tablename__ = 'TBL_ROLE'


class Slider(Base):
    id = Column(Integer, primary_key=True, index=True)

    slider_binary_id = Column(Integer, ForeignKey("TBL_BINARY.id"))
    lab_id = Column(Integer, ForeignKey("TBL_LAB.id"))
    is_active = Column(Boolean)
    #created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))
    created_at = Column(DateTime(timezone=False), default=datetime.datetime.utcnow)

    __tablename__ = 'TBL_SLIDER'


class Events(Base):
    id = Column(Integer, primary_key=True, index=True)

    lab_id = Column(Integer, ForeignKey("TBL_LAB.id"))
    title = Column(String)
    description = Column(String)
    binary_id = Column(Integer, ForeignKey("TBL_BINARY.id"))
    event_date = Column(Date)
    created_at = Column(DateTime(timezone=False), default=datetime.datetime.utcnow) 
    #created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))
    is_active = Column(Boolean)

    __tablename__ = 'TBL_EVENTS'


class Patent(Base):
    id = Column(Integer, primary_key=True, index=True)

    publication_id = Column(Integer, ForeignKey("TBL_PUBLICATION.id"))
    description = Column(String)
    lab_id = Column(Integer, ForeignKey("TBL_LAB.id"))
    created_at = Column(DateTime(timezone=False), default=datetime.datetime.utcnow) 
    #created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))
    is_active = Column(Boolean)

    __tablename__ = 'TBL_PATENT'


class PosterDemo(Base):
    id = Column(Integer, primary_key=True, index=True)

    lab_id = Column(Integer, ForeignKey("TBL_LAB.id"))
    binary_id = Column(Integer, ForeignKey("TBL_BINARY.id"))
    description = Column(String)
    created_at = Column(DateTime(timezone=False), default=datetime.datetime.utcnow) 
    #created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))
    is_active = Column(Boolean)
    type = Column(String)

    __tablename__ = 'TBL_POSTER_DEMO'

class Gallery(Base):
    id = Column(Integer,primary_key=True, index=True )

    event_id = Column(Integer, ForeignKey("TBL_EVENTS.id"))
    binary_id = Column(Integer, ForeignKey("TBL_BINARY.id"))

    __tablename__ = 'TBL_GALLERY'


class Feedback(Base):
    id = Column(Integer,primary_key=True, index=True )
    name = Column(String)
    email = Column(String)
    subject = Column(String)
    message = Column(String)
    lab_id = Column(Integer, ForeignKey("TBL_LAB.id"))
    created_at = Column(DateTime(timezone=False), default=datetime.datetime.utcnow) 


    __tablename__ = 'TBL_FEEDBACK'


