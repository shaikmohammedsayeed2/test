import models
from tests.base import *
from fastapi.encoders import jsonable_encoder




# Unit test for lab retrieval
def test_get_lab():
    # Create a new lab helper function
    response = create_new_lab()
    
    # Check for status code 
    assert response.status_code == 200

    lab_id = response.json()
    
    # Check the lab get api
    response = client.get("/home/{0}".format(lab_id))
    assert response.status_code == 200



# Unit test for lab insertion
def test_create_lab():
    # Create a new lab helper function
    response = create_new_lab()

    lab_id = response.json()
    # Check for status code 
    assert response.status_code == 200

    # Query mock db for lab insertion
    with TestingSessionLocal() as mock_db:
        lab = mock_db.query(models.Lab).filter(models.Lab.id == lab_id).first()
        assert lab and lab.id == lab_id


# Unit test for lab update
def test_update_lab():
    # Create a new lab
    response = create_new_lab()

    lab_id = response.json()
    assert response.status_code == 200

    # Get the instance by querying db

    with TestingSessionLocal() as mock_db:
        lab = mock_db.query(models.Lab).filter(models.Lab.id == lab_id).first()
        lab.name = "Updated name"
        lab.overview = "Updated overview"
        lab.address = "Updated address"
        lab.email = "Updated email"
        lab.phone = "Updated phone"
        lab.twitter_handle = "Updated twitter handle"

        # Update using the Update API
        response = client.put(
            "/lab/{0}".format(lab_id),
            json=jsonable_encoder(lab)
        )
        assert response.status_code == 200

        # Query mock db for lab updation

        n_lab = mock_db.query(models.Lab).filter(models.Lab.id == lab_id).first()

        assert lab.name == n_lab.name
        assert lab.overview == n_lab.overview
        assert lab.address == n_lab.address
        assert lab.email == n_lab.email
        assert lab.phone == n_lab.phone
        assert lab.twitter_handle == n_lab.twitter_handle
    
    # Test is done



# Unit test for lab deletion
def test_delete_lab():
    # Create a new lab
    response = create_new_lab()

    lab_id = response.json()
    assert response.status_code == 200

    # Delte using the Delete API
    
    response = client.delete(
        "/lab?lab_id={0}".format(lab_id)
    )
    assert response.status_code == 200

    # Query mock db for confirming lab deletion

    # Get the instance by querying db
    with TestingSessionLocal() as mock_db:
        lab = mock_db.query(models.Lab).filter(models.Lab.id == lab_id).first()
        assert lab is None




# Unittest for Lab Creation access levels
def test_create_lab_access_levels():
    # No access other than Admin
    response = create_new_lab(unauthorized_jwt_token)
    assert response.status_code == 401

    token = create_auth_token("manager")
    response = create_new_lab(token)
    assert response.status_code == 401

    token = create_auth_token("user")
    response = create_new_lab(token)
    assert response.status_code == 401


# Unittest for Lab Update access levels
def test_update_lab_Access_levels():
    # Create a new lab
    response = create_new_lab()

    lab_id = response.json()
    assert response.status_code == 200

    with TestingSessionLocal() as mock_db:
        lab = mock_db.query(models.Lab).filter(models.Lab.id == lab_id).first()

    
        # No access other than Admin and manager of the lab
        # Manager of the lab
        token = create_auth_token("manager",lab_id)
        client.cookies.set(COOKIE_KEY, token)
        response = client.put("/lab/{0}".format(lab_id),json=jsonable_encoder(lab))
        assert response.status_code == 200

        # Manager of other lab
        token = create_auth_token("manager",lab_id-1)
        client.cookies.set(COOKIE_KEY, token)
        response = client.put("/lab/{0}".format(lab_id),json=jsonable_encoder(lab))
        assert response.status_code == 401

        # Any User
        token = create_auth_token("user")
        client.cookies.set(COOKIE_KEY, token)
        response = client.put("/lab/{0}".format(lab_id),json=jsonable_encoder(lab))
        assert response.status_code == 401


# Unittest for Lab Deletion access levels
def test_delete_lab_access_levels():
    # Create a new lab
    response = create_new_lab()
    lab_id = response.json()
    assert response.status_code == 200
    # Delte using the Delete API
    
    response = client.delete(
        "/lab?lab_id={0}".format(lab_id)
    )
    assert response.status_code == 200

    # Query mock db for confirming lab deletion

    # Get the instance by querying db
    with TestingSessionLocal() as mock_db:
        lab = mock_db.query(models.Lab).filter(models.Lab.id == lab_id).first()
        assert lab is None

        # No access for any other than Admin 
        token = create_auth_token("manager")
        client.cookies.set(COOKIE_KEY, token)
        response = client.delete("/lab?lab_id={0}".format(lab_id))        
        assert response.status_code == 401

        # Any User
        token = create_auth_token("user")
        client.cookies.set(COOKIE_KEY, token)
        response = client.delete("/lab?lab_id={0}".format(lab_id))        
        assert response.status_code == 401