import models
from tests.base import *
from fastapi.encoders import jsonable_encoder

def create_new_publication(lab_id:int):
    pub_data = {
        "pub_title": "Test_pub",
        "description": "Pub_Description",
        "lab_id": lab_id,
        "type": "journal",
        "pub_date": "2023-04-29",
        "pub_pdf": "string"
    }

    response = client.post(
        "/publication",
        json=pub_data
    )

    return response

# Unit test for publication retrieval
def test_get_publication():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    pub_response = create_new_publication(lab_id)
    
    # Check for status code
    assert pub_response.status_code == 200
    
    publication_id = pub_response.json()
    
    # Check the publication get api
    response = client.get("/publications/{0}".format(lab_id))
    assert response.status_code == 200

# Unit test for publication insertion
def test_create_publication():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    pub_response = create_new_publication(lab_id)
    
    # Check for status code
    assert pub_response.status_code == 200
    
    publication_id = pub_response.json()
    
    # Query mock db for publication insertion
    with TestingSessionLocal() as mock_db:
        publication = mock_db.query(models.Publication).filter(models.Publication.id == publication_id).first()
        assert publication and publication.id == publication_id

# Unit test for publication update
def test_update_publication():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    pub_response = create_new_publication(lab_id)
    
    # Check for status code
    assert pub_response.status_code == 200
    
    publication_id = pub_response.json()
    
    # Get the instance by querying db
    
    with TestingSessionLocal() as mock_db:
        publication = mock_db.query(models.Publication).filter(models.Publication.id == publication_id).first()
        publication.pub_title = "Updated name"
        publication.description = "Updated description"
        
        # Update using the Update API
        response = client.put(
            "/publication/{0}".format(publication_id),
            json = jsonable_encoder(publication)
        )
        assert response.status_code == 200
        
        updated_pub = mock_db.query(models.Publication).filter(models.Publication.id == publication_id).first()
        
        assert publication.pub_title == updated_pub.pub_title
        assert publication.description == updated_pub.description
    
    # Test is done

# Unit test for publication deletion
def test_delete_publication():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    pub_response = create_new_publication(lab_id)
    
    # Check for status code
    assert pub_response.status_code == 200
    
    publication_id = pub_response.json()
    
    # Delete using the Delete API
    
    response = client.delete(
        "/publication?publication_id={0}".format(publication_id)
    )
    assert response.status_code == 200
    
    # Query mock db for confirming publication deletion
    
    # get the instance by querying db
    with TestingSessionLocal() as mock_db:
        publication = mock_db.query(models.Publication).filter(models.Publication.id == publication_id).first()
        assert publication is None        
            