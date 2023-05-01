import models
from tests.base import *
from fastapi.encoders import jsonable_encoder

def create_new_conference(lab_id:int):
    conf_data = {
        "conf_title": "Test_conf",
        "description": "Conf_Description",
        "lab_id": lab_id,
        "start_date": "2023-04-21",
        "end_date": "2023-04-29",
        "conf_pdf": "string"
    }

    response = client.post(
        "/conference",
        json=conf_data
    )

    return response


# Unit test for conference retrieval
def test_get_conference():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    conf_response = create_new_conference(lab_id)
    
    # Check for status code
    assert conf_response.status_code == 200
    
    conference_id = conf_response.json()
    
    # Check the conference get api
    response = client.get("/conferences/{0}".format(lab_id))
    assert response.status_code == 200

# Unit test for conference insertion
def test_create_conference():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    conf_response = create_new_conference(lab_id)
    
    # Check for status code
    assert conf_response.status_code == 200
    
    conference_id = conf_response.json()
    
    # Query mock db for conference insertion
    with TestingSessionLocal() as mock_db:
        conference = mock_db.query(models.Conference).filter(models.Conference.id == conference_id).first()
        assert conference and conference.id == conference_id

# Unit test for conference update
def test_update_conference():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    conf_response = create_new_conference(lab_id)
    
    # Check for status code
    assert conf_response.status_code == 200
    
    conference_id = conf_response.json()
    
    # Get the instance by querying db
    
    with TestingSessionLocal() as mock_db:
        conference = mock_db.query(models.Conference).filter(models.Conference.id == conference_id).first()
        conference.conf_title = "Updated name"
        conference.description = "Updated description"
        
        # Update using the Update API
        response = client.put(
            "/conference/{0}".format(conference_id),
            json = jsonable_encoder(conference)
        )
        assert response.status_code == 200
        
        updated_conf = mock_db.query(models.Conference).filter(models.Conference.id == conference_id).first()
        
        assert conference.conf_title == updated_conf.conf_title
        assert conference.description == updated_conf.description
    
    # Test is done

# Unit test for conference deletion
def test_delete_conference():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    conf_response = create_new_conference(lab_id)
    
    # Check for status code
    assert conf_response.status_code == 200
    
    conference_id = conf_response.json()
    
    # Delete using the Delete API
    
    response = client.delete(
        "/conference?conf_id={0}".format(conference_id)
    )
    assert response.status_code == 200
    
    # Query mock db for confirming conference deletion
    
    # get the instance by querying db
    with TestingSessionLocal() as mock_db:
        conference = mock_db.query(models.Conference).filter(models.Conference.id == conference_id).first()
        assert conference is None        
            