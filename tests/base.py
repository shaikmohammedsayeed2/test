from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from session import COOKIE_KEY, RleSession, JWT_SCERET
from database import Base
from main import app
from utils import get_db,USER_ROLE
import jwt

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Pass%40Po-es.15@127.0.0.1/rm_test1"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)

# Creates token based on role and lab and person ids
def create_auth_token(role,lab_id=1,person_id=1):
    jwt_payload = {
            "userid": "demo@iith.ac.in",
            "name": "Test name",
            "email": "Email",
            "role_id": USER_ROLE[role],
            "lab_id": lab_id,
            "person_id": person_id,
            "role_name": role
        }
    # Creating a JWT and send cookie
    jwt_token = jwt.encode(jwt_payload, JWT_SCERET, algorithm="HS256")
    return jwt_token


authorized_jwt_token_admin = create_auth_token("admin")
unauthorized_jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiIxMDU3MTI1NTkyNTA4NDQ0MTI3ODUiLCJuYW1lIjoiUEVMTFVSSSBTUklWQVJESEFOIiwiZW1haWwiOiJjczE5YnRlY2gxMTA1MkBpaXRoLmFjLmluIiwicm9sZV9pZCI6MSwicGVyc29uX2lkIjoxNCwicm9sZV9uYW1lIjoiYWRtaW4ifQ.I1chegt1hmkZ8B6lAGsJLJZymajPqQTNGlHW3H2Di6"

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# Helper method for lab creation
def create_new_lab(cookie=authorized_jwt_token_admin):
    lab_data = {
        "name": "Test_lab",
        "overview": "Overview",
        "address": "address",
        "email": "email",
        "phone": "phone",
        "twitter_handle": "string",
        "lab_logo_url": "string",
        "lab_cover_url": "string"
    }

    client.cookies.set(COOKIE_KEY, cookie)

    response = client.post(
        "/lab",
        json=lab_data
    )

    return response


