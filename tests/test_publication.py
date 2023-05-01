import models
from tests.base import *
from fastapi.encoders import jsonable_encoder

def create_new_publication(lab_id:int,auth_cookie):
    pub_data = {
        "pub_title": "Test_pub",
        "description": "Pub_Description",
        "lab_id": lab_id,
        "type": "journal",
        "pub_date": "2023-04-29",
        "pub_pdf": "string"
    }
    
    client.cookies.set(COOKIE_KEY, auth_cookie)

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
    
    pub_response = create_new_publication(lab_id,authorized_jwt_token_admin)
    
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
    
    pub_response = create_new_publication(lab_id,authorized_jwt_token_admin)
    
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
    
    pub_response = create_new_publication(lab_id,authorized_jwt_token_admin)
    
    # Check for status code
    assert pub_response.status_code == 200
    
    publication_id = pub_response.json()
    
    # Get the instance by querying db
    
    with TestingSessionLocal() as mock_db:
        publication = mock_db.query(models.Publication).filter(models.Publication.id == publication_id).first()
        publication.pub_title = "Updated name"
        publication.description = "Updated description"
        publication.pub_binary_id = publication.pub_binary_id
        publication.lab_id = lab_id
        publication.pub_date = "2023-05-02"
        publication.type = "conference"
        
        # Update using the Update API
        response = client.put(
            "/publication/{0}".format(publication_id),
            json = jsonable_encoder(publication)
        )
        assert response.status_code == 200
        
        updated_pub = mock_db.query(models.Publication).filter(models.Publication.id == publication_id).first()
        
        assert publication.pub_title == updated_pub.pub_title
        assert publication.description == updated_pub.description
        assert publication.pub_binary_id == updated_pub.pub_binary_id
        assert publication.lab_id == updated_pub.lab_id
        assert publication.pub_date == updated_pub.pub_date
        assert publication.type == updated_pub.type
        
    # Test is done

# Unit test for publication deletion
def test_delete_publication():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    pub_response = create_new_publication(lab_id,authorized_jwt_token_admin)
    
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



def test_create_publication_access_levels():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    # Create a new publication Unauthorized
    pub_response = create_new_publication(lab_id,unauthorized_jwt_token)
    assert pub_response.status_code == 401
    
    # Create a new publication Unauthorized
    pub_response = create_new_publication(lab_id,authorized_jwt_token_user)
    assert pub_response.status_code == 401
 
 
    
def test_update_publication_access_levels():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    pub_response = create_new_publication(lab_id,authorized_jwt_token_admin)
    
    # Check for status code
    assert pub_response.status_code == 200
    
    publication_id = pub_response.json()
    
    # Get the instance by querying db
    
    with TestingSessionLocal() as mock_db:
        publication = mock_db.query(models.Publication).filter(models.Publication.id == publication_id).first()
        publication.pub_title = "Updated name"
        publication.description = "Updated description"
        publication.pub_binary_id = publication.pub_binary_id
        publication.lab_id = lab_id
        publication.pub_date = "2023-05-02"
        publication.type = "conference"
        
        # Unauthorized\
        client.cookies.set(COOKIE_KEY, unauthorized_jwt_token)
        response = client.put(
            "/publication/{0}".format(publication_id),
            json = jsonable_encoder(publication)
        )
        assert response.status_code == 401
        
        # Unauthorized\
        client.cookies.set(COOKIE_KEY, authorized_jwt_token_user)
        response = client.put(
            "/publication/{0}".format(publication_id),
            json = jsonable_encoder(publication)
        )
        assert response.status_code == 401
 
def test_delete_publication_access_levels():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    pub_response = create_new_publication(lab_id,authorized_jwt_token_admin)
    
    # Check for status code
    assert pub_response.status_code == 200
    
    publication_id = pub_response.json()
    
    # Unauthorized
    client.cookies.set(COOKIE_KEY, unauthorized_jwt_token)
    response = client.delete(
        "/publication?publication_id={0}".format(publication_id)
    )
    assert response.status_code == 401  
    
    # Unauthorized
    client.cookies.set(COOKIE_KEY, authorized_jwt_token_user)
    response = client.delete(
        "/publication?publication_id={0}".format(publication_id)
    )
    assert response.status_code == 401        
                  