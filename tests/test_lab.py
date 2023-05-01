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

    # Get the instance by querying db

    with TestingSessionLocal() as mock_db:
        lab = mock_db.query(models.Lab).filter(models.Lab.id == lab_id).first()
        lab.name = "Updated name"
        lab.overview = "Updated overview"

        # Update using the Update API
        response = client.put(
            "/lab/{0}".format(lab_id),
            json=jsonable_encoder(lab)
        )
        assert response.status_code == 200

        # Query mock db for lab updation
        #mock_db.add(lab)
        #mock_db.commit()

        n_lab = mock_db.query(models.Lab).filter(models.Lab.id == lab_id).first()

        assert lab.name == n_lab.name
        assert lab.overview == n_lab.overview
    
    # Test is done



# Unit test for lab deletion
def test_delete_lab():
    # Create a new lab
    response = create_new_lab()

    lab_id = response.json()

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

