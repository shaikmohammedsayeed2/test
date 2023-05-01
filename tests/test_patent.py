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

def create_new_patent(pub_id:int,lab_id:int):
    patent_data = {
        "publication_id": pub_id,
        "description": "Patent description",
        "lab_id": lab_id
    }
    
    response = client.post(
        "/patent",
        json=patent_data
    )
    
    return response  

# Unit test for patent insertion
def test_create_patent():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    pub_response = create_new_publication(lab_id)
    
    # Check for status code
    assert pub_response.status_code == 200
    
    publication_id = pub_response.json()
    
    patent_response = create_new_patent(publication_id, lab_id)
    
    # Check for status code
    assert patent_response.status_code == 200
    
    patent_id = patent_response.json()
    
    # Query mock db for patent insertion
    with TestingSessionLocal() as mock_db:
        patent = mock_db.query(models.Patent).filter(models.Patent.id == patent_id).first()
        assert patent and patent.id == patent_id

# Unit test for patent update
def test_update_patent():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    pub_response = create_new_publication(lab_id)
    
    # Check for status code
    assert pub_response.status_code == 200
    
    publication_id = pub_response.json()
    
    patent_response = create_new_patent(publication_id, lab_id)
    
    # Check for status code
    assert patent_response.status_code == 200
    
    patent_id = patent_response.json()
    
    # Get the instance by querying db
    
    with TestingSessionLocal() as mock_db:
        patent = mock_db.query(models.Patent).filter(models.Patent.id == patent_id).first()
        patent.description = "Updated description"
        
        # Update using the Update API
        response = client.put(
            "/patent/{0}".format(patent_id),
            json = jsonable_encoder(patent)
        )
        assert response.status_code == 200
        
        updated_patent = mock_db.query(models.Patent).filter(models.Patent.id == patent_id).first()
        
        assert patent.description == updated_patent.description
    
    # Test is done

# Unit test for patent deletion
def test_delete_patent():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    pub_response = create_new_publication(lab_id)
    
    # Check for status code
    assert pub_response.status_code == 200
    
    publication_id = pub_response.json()
    
    patent_response = create_new_patent(publication_id, lab_id)
    
    # Check for status code
    assert patent_response.status_code == 200
    
    patent_id = patent_response.json()
    
    # Delete using the Delete API
    
    response = client.delete(
        "/patent?patent_id={0}".format(patent_id)
    )
    assert response.status_code == 200
    
    # Query mock db for confirming patent deletion
    
    # get the instance by querying db
    with TestingSessionLocal() as mock_db:
        patent = mock_db.query(models.Patent).filter(models.Patent.id == patent_id).first()
        assert patent is None        
            