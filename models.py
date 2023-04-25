from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base


class Binary(Base):
    id = Column(Integer, primary_key=True, index=True)

    blob_storage = Column(String)
    blob_size = Column(Integer)
    is_active = Column(Boolean)
    created_by = Column(Integer, ForeignKey("TBL_PERSON.id")) 
    created_at = Column(DateTime)

    __tablename__ = 'TBL_BINARY'


class Conference(Base):
    id = Column(Integer, primary_key=True, index=True)

    conf_title = Column(String)
    description = Column(String)
    conf_binary_id = Column(Integer, ForeignKey("TBL_BINARY.id"))
    lab_id = Column(Integer, ForeignKey("TBL_LAB.id"))
    is_active = Column(Boolean)
    created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))
    created_at = Column(DateTime)

    __tablename__ = 'TBL_CONFERENCE'


class ContactUs(Base):
    id = Column(Integer, primary_key=True, index=True)

    address = Column(String)
    email = Column(String)
    phone = Column(String)
    is_active = Column(Boolean)
    created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))
    created_at = Column(DateTime)

    __tablename__ = 'TBL_CONTACT_US'


class Lab(Base):
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    lab_logo_id = Column(Integer, ForeignKey("TBL_BINARY.id"))
    overview = Column(String)
    contact_id = Column(Integer, ForeignKey("TBL_CONTACT_US.id"))
    is_active = Column(Boolean)
    created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))
    created_at = Column(DateTime)

    ## Relation
    # _lab_members = relationship("LabMember")
    _lab_members = relationship("LabMember")

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
    created_at = Column(DateTime)
    profile_binary_id = Column(Integer, ForeignKey("TBL_BINARY.id"))
    created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))


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
    created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))
    created_at = Column(DateTime)
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
    created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))
    created_at = Column(DateTime)

    __tablename__ = 'TBL_SLIDER'


class Events(Base):
    id = Column(Integer, primary_key=True, index=True)

    lab_id = Column(Integer, ForeignKey("TBL_LAB.id"))
    title = Column(String)
    description = Column(String)
    binary_id = Column(Integer, ForeignKey("TBL_BINARY.id"))
    created_at = Column(DateTime) 
    created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))
    is_active = Column(Boolean)

    __tablename__ = 'TBL_EVENTS'


class Patent(Base):
    id = Column(Integer, primary_key=True, index=True)

    publication_id = Column(Integer, ForeignKey("TBL_PUBLICATION.id"))
    description = Column(String)
    lab_id = Column(Integer, ForeignKey("TBL_LAB.id"))
    created_at = Column(DateTime) 
    created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))
    is_active = Column(Boolean)

    __tablename__ = 'TBL_PATENT'


class PosterDemo(Base):
    id = Column(Integer, primary_key=True, index=True)

    lab_id = Column(Integer, ForeignKey("TBL_LAB.id"))
    binary_id = Column(Integer, ForeignKey("TBL_BINARY.id"))
    description = Column(String)
    created_at = Column(DateTime) 
    created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))
    is_active = Column(Boolean)
    type = Column(String)

    __tablename__ = 'TBL_POSTER_DEMO'