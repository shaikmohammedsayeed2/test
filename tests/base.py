from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from session import COOKIE_KEY
from database import Base
from main import app
from utils import get_db

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Pass%40Po-es.15@127.0.0.1/rm_test1"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


authorized_jwt_token_admin = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiIxMDU3MTI1NTkyNTA4NDQ0MTI3ODUiLCJuYW1lIjoiUEVMTFVSSSBTUklWQVJESEFOIiwiZW1haWwiOiJjczE5YnRlY2gxMTA1MkBpaXRoLmFjLmluIiwicm9sZV9pZCI6MSwicGVyc29uX2lkIjoxNCwicm9sZV9uYW1lIjoiYWRtaW4ifQ.I1chegt1hmkZ8B6lAGsJLJZymajPqQTNGlHW3H2Di6I"
authorized_jwt_token_manager = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiIxMDU3MTI1NTkyNTA4NDQ0MTI3ODUiLCJuYW1lIjoiUEVMTFVSSSBTUklWQVJESEFOIiwiZW1haWwiOiJjczE5YnRlY2gxMTA1MkBpaXRoLmFjLmluIiwicm9sZV9pZCI6MiwicGVyc29uX2lkIjoxNCwicm9sZV9uYW1lIjoibWFuYWdlciJ9.pj1eQFstdkmIeJLWQkpkoBtP80pRxe0QVkjxptJy9Rc"
authorized_jwt_token_user = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiIxMDU3MTI1NTkyNTA4NDQ0MTI3ODUiLCJuYW1lIjoiUEVMTFVSSSBTUklWQVJESEFOIiwiZW1haWwiOiJjczE5YnRlY2gxMTA1MkBpaXRoLmFjLmluIiwicm9sZV9pZCI6MywicGVyc29uX2lkIjoxNCwicm9sZV9uYW1lIjoidXNlciJ9.PUeyESLKUHyovGoiRUDVtCbc2RJ0ZXa4TUQcEKau28s"

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
def create_new_lab():
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

    client.cookies.set(COOKIE_KEY, authorized_jwt_token_admin)

    response = client.post(
        "/lab",
        json=lab_data
    )

    return response