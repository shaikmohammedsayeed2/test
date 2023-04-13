from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base


class Binary(Base):
    id = Column(Integer, primary_key=True, index=True)

    blob_size = Column(Integer)
    is_active = Column(Boolean)
    created_by = Column(Integer, ForeignKey("TBL_PERSON.id")) 
    created_at = Column(DateTime)
    blob_storage = Column(String)

    __tablename__ = 'TBL_BINARY'


class Conference(Base):
    id = Column(Integer, primary_key=True, index=True)

    conf_title = Column(String)
    description = Column(String)
    is_active = Column(Boolean)
    created_at = Column(DateTime)
    conf_binary_id = Column(Integer, ForeignKey("TBL_BINARY.id"))
    lab_id = Column(Integer, ForeignKey("TBL_LAB.id"))
    created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))

    __tablename__ = 'TBL_CONFERENCE'


class ContactUs(Base):
    id = Column(Integer, primary_key=True, index=True)

    address = Column(String)
    email = Column(String)
    phone = Column(String)
    is_active = Column(Boolean)
    created_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))

    __tablename__ = 'TBL_CONTACT_US'


class Lab(Base):
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    overview = Column(String)
    is_active = Column(Boolean)
    created_at = Column(DateTime)
    lab_logo_id = Column(Integer, ForeignKey("TBL_BINARY.id"))
    contact_id = Column(Integer, ForeignKey("TBL_CONTACT_US.id"))
    created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))

    __tablename__ = 'TBL_LAB'


class LabMember(Base):
    id = Column(Integer, primary_key=True, index=True)

    person_id = Column(Integer, ForeignKey("TBL_PERSON.id"))
    lab_id = Column(Integer, ForeignKey("TBL_LAB.id"))
    role_id = Column(Integer, ForeignKey("TBL_ROLE.id"))
    person_role_id = Column(Integer, ForeignKey("TBL_PERSON_ROLE.id"))

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
    profile_binary = Column(Integer, ForeignKey("TBL_BINARY.id"))
    created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))

    labs = relationship("LabMember")

    __tablename__ = 'TBL_PERSON'


class PersonRole(Base):
    id = Column(Integer, primary_key=True, index=True)

    is_active = Column(Boolean)
    person_role_name = Column(String)  # This field type is a guess.

    __tablename__ = 'TBL_PERSON_ROLE'


class Publication(Base):
    id = Column(Integer, primary_key=True, index=True)

    pub_title = Column(String)
    description = Column(String)
    created_at = Column(DateTime)
    pub_binary_id = Column(Integer, ForeignKey("TBL_BINARY.id"))
    lab_id = Column(Integer, ForeignKey("TBL_LAB.id"))
    created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))

    __tablename__ = 'TBL_PUBLICATION'


class Role(Base):
    id = Column(Integer, primary_key=True, index=True)

    is_active = Column(Boolean)
    role_name = Column(String)  

    __tablename__ = 'TBL_ROLE'


class Slider(Base):
    id = Column(Integer, primary_key=True, index=True)

    is_active = Column(Boolean)
    created_at = Column(DateTime)
    slider_binary_id = Column(Integer, ForeignKey("TBL_BINARY.id"))
    lab_id = Column(Integer, ForeignKey("TBL_LAB.id"))
    created_by = Column(Integer, ForeignKey("TBL_PERSON.id"))

    __tablename__ = 'TBL_SLIDER'

