import models
from tests.base import *
from fastapi.encoders import jsonable_encoder

def create_new_event(lab_id:int,auth_cookie):
    event_data = {
        "lab_id": lab_id,
        "title": "Event_Title",
        "description": "Event_Description",
        "event_date": "2023-04-29",
        "event_image": "string"
    }
    
    client.cookies.set(COOKIE_KEY, auth_cookie)

    response = client.post(
        "/event",
        json=event_data
    )

    return response



# Unit test for event retrieval
def test_get_event():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    event_response = create_new_event(lab_id,authorized_jwt_token_admin)
    
    # Check for status code
    assert event_response.status_code == 200
    
    event_id = event_response.json()
    
    # Check the publication get api
    response = client.get("/event/{0}".format(lab_id))
    assert response.status_code == 200

# Unit test for event insertion
def test_create_event():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    event_response = create_new_event(lab_id,authorized_jwt_token_admin)
    
    # Check for status code
    assert event_response.status_code == 200
    
    event_id = event_response.json()
    
    # Query mock db for event insertion
    with TestingSessionLocal() as mock_db:
        event = mock_db.query(models.Events).filter(models.Events.id == event_id).first()
        assert event and event.id == event_id



# Unit test for event update
def test_update_event():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    event_response = create_new_event(lab_id,authorized_jwt_token_admin)
    
    # Check for status code
    assert event_response.status_code == 200
    
    event_id = event_response.json()
    
    # Get the instance by querying db
    
    with TestingSessionLocal() as mock_db:
        event = mock_db.query(models.Events).filter(models.Events.id == event_id).first()
        event.lab_id = lab_id
        event.title = "Updated title"
        event.description = "Updated Description"
        event.event_date = "2023-05-01"
        event.binary_id = event.binary_id
        
        response = client.put(
            "/event/{0}".format(event_id),
            json = jsonable_encoder(event)
        )
        assert response.status_code == 200
        
        updated_event = mock_db.query(models.Events).filter(models.Events.id == event_id).first()
        
        assert event.lab_id == updated_event.lab_id
        assert event.title == updated_event.title
        assert event.description == updated_event.description
        assert event.event_date == updated_event.event_date
        assert event.binary_id == updated_event.binary_id
        


def test_delete_event():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    event_response = create_new_event(lab_id,authorized_jwt_token_admin)
    
    # Check for status code
    assert event_response.status_code == 200
    
    event_id = event_response.json()
    
    response = client.delete(
        "/event?event_id={0}".format(event_id)
    )
    assert response.status_code == 200
    
    with TestingSessionLocal() as mock_db:
        event = mock_db.query(models.Events).filter(models.Events.id==event_id).first()
        assert event is None



def test_create_event_access_levels():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    # Create a new event unauthorized
    event_response = create_new_event(lab_id,unauthorized_jwt_token)
    assert event_response.status_code == 401
    
    # Create a new event by user of same lab
    cookie = create_auth_token("user",lab_id)
    event_response = create_new_event(lab_id,cookie)
    assert event_response.status_code == 200
    
    # Create a new event by user of different lab
    cookie = create_auth_token("user",lab_id-1)
    event_response = create_new_event(lab_id,cookie)
    assert event_response.status_code == 401
    
    # Create a new event by manager of same lab
    cookie = create_auth_token("manager",lab_id)
    event_response = create_new_event(lab_id,cookie)
    assert event_response.status_code == 200
    
    # Create a new event by manager of different lab
    cookie = create_auth_token("manager",lab_id-1)
    event_response = create_new_event(lab_id,cookie)
    assert event_response.status_code == 401

def test_update_event_access_levels():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    event_response = create_new_event(lab_id,authorized_jwt_token_admin)
    
    # Check for status code
    assert event_response.status_code == 200
    
    event_id = event_response.json()
    
    # Get the instance by querying db
    
    with TestingSessionLocal() as mock_db:
        event = mock_db.query(models.Events).filter(models.Events.id == event_id).first()
        assert event is not None
        
        # Unauthorized
        client.cookies.set(COOKIE_KEY, unauthorized_jwt_token)
        response = client.put(
            "/event/{0}".format(event_id),
            json = jsonable_encoder(event)
        )
        assert response.status_code == 401
        
        # Update by user of same lab
        cookie = create_auth_token("user",lab_id)
        client.cookies.set(COOKIE_KEY, cookie)
        response = client.put(
            "/event/{0}".format(event_id),
            json = jsonable_encoder(event)
        )
        assert response.status_code == 200
        
        # Update by user of different lab
        cookie = create_auth_token("user",lab_id-1)
        client.cookies.set(COOKIE_KEY, cookie)
        response = client.put(
           "/event/{0}".format(event_id),
           json = jsonable_encoder(event)
        )
        assert response.status_code == 401
        
        # Update by manager of same lab
        cookie = create_auth_token("manager",lab_id)
        client.cookies.set(COOKIE_KEY, cookie)
        response = client.put(
            "/event/{0}".format(event_id),
            json = jsonable_encoder(event)
        )
        assert response.status_code == 200
        
        # Update by manager of different lab
        cookie = create_auth_token("manager",lab_id-1)
        client.cookies.set(COOKIE_KEY, cookie)
        response = client.put(
           "/event/{0}".format(event_id),
           json = jsonable_encoder(event)
        )
        assert response.status_code == 401

def test_delete_event_access_levels():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    event_response = create_new_event(lab_id,authorized_jwt_token_admin)
    
    # Check for status code
    assert event_response.status_code == 200
    
    event_id = event_response.json()
    
    # Unauthorized
    client.cookies.set(COOKIE_KEY, unauthorized_jwt_token)
    response = client.delete(
        "/event?event_id={0}".format(event_id)
    )
    assert response.status_code == 401
    
    # Delete by manager of different lab
    cookie = create_auth_token("manager",lab_id-1)
    client.cookies.set(COOKIE_KEY, cookie)
    response = client.delete(
       "/event?event_id={0}".format(event_id)
    )
    assert response.status_code == 401 
    
    # Delete by manager of same lab
    cookie = create_auth_token("manager",lab_id)
    client.cookies.set(COOKIE_KEY, cookie)
    response = client.delete(
        "/event?event_id={0}".format(event_id)
    )
    assert response.status_code == 200
                           
        