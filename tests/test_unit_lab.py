import sqlalchemy
from session import COOKIE_KEY
import pytest

from tests.base import client, authorized_jwt_token, unauthorized_jwt_token

lab_id = None
event_id = None

@pytest.fixture
def context():
      return {}

@pytest.mark.order(1)
def test_create_lab(context):
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
        json=lab_data
    )
    assert response.status_code == 200
    #context['lab_id'] = response.json()
    global lab_id
    lab_id = response.json()


@pytest.mark.order(2)
# Test post event
def test_post_event_with_invalid_labid(context):
    event_data = {
        "lab_id": -1,
        "title": "Test event",
        "description": "Added only for testing",
        "event_date": "2023-04-29",
        "event_image": "https://lh3.googleusercontent.com/a/AGNmyxbc4CUwq9DEt0BsPYtO_vTHdAJ161B-UqUg_cJH-Q=s96-c"
    }

    client.cookies.set(COOKIE_KEY, authorized_jwt_token)
    with pytest.raises(sqlalchemy.exc.IntegrityError, match="ForeignKeyViolation"):
        response = client.post(
            "/event",
            json=event_data
        )

@pytest.mark.order(3)
# Test post event
def test_post_event_with_valid_labid(context):
    # print(context.get("lab_id"))
    global lab_id
    event_data = {
        "lab_id": lab_id,
        "title": "Test event",
        "description": "Added only for testing",
        "event_date": "2023-04-29",
        "event_image": "https://lh3.googleusercontent.com/a/AGNmyxbc4CUwq9DEt0BsPYtO_vTHdAJ161B-UqUg_cJH-Q=s96-c"
    }

    client.cookies.set(COOKIE_KEY, authorized_jwt_token)
    
    response = client.post(
        "/event",
        json=event_data
    )
    global event_id
    assert response.status_code == 200
    event_id = response.json()


@pytest.mark.order(4)
def test_delete_lab_with_valid_id(context):
    global lab_id
    resposne = client.delete(
        "/lab?lab_id={lab_id}"
    )


@pytest.mark.order(5)
def test_delete_lab_with_invalid_id(context):
    with pytest.raises(AttributeError):
        resposne = client.delete(
            "/lab?lab_id=-1"
        )

@pytest.mark.order(6)
def test_delete_event_with_invalid_access(context):
    client.cookies.set(COOKIE_KEY,unauthorized_jwt_token )
    global event_id
    
    resposne = client.delete(
        "/event?event_id={event_id}"
    )

@pytest.mark.order(7)
def test_delete_event_with_valid_access(context):
    client.cookies.set(COOKIE_KEY, authorized_jwt_token)
    global event_id
    
    resposne = client.delete(
        "/event?event_id={event_id}"
    )