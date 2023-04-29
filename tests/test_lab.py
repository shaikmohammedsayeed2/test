from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from main import app
from utils import get_db
from session import COOKIE_KEY, JWT_SCERET


from base import client, authorized_jwt_token


def test_create_lab():
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

    response = client.post(
        "/lab",
        json=lab_data,
        cookies={COOKIE_KEY:authorized_jwt_token}
    )
    assert response.status_code == 200



def test_post_event():
    event_data = {
        "lab_id": 7,
        "title": "Test event",
        "description": "Added only for testing",
        "event_date": "2023-04-29",
        "event_image": "https://lh3.googleusercontent.com/a/AGNmyxbc4CUwq9DEt0BsPYtO_vTHdAJ161B-UqUg_cJH-Q=s96-c"
    }

    response = client.post(
        "/event",
        json=event_data,
        cookies={COOKIE_KEY:authorized_jwt_token}
    )
    assert response.status_code != 200
