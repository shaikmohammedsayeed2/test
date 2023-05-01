import models
from tests.base import *
from fastapi.encoders import jsonable_encoder


def create_feedback(labid):
    feedback_data = {
        "lab_id": labid,
        "name": "string",
        "email": "string",
        "subject": "string",
        "message": "string"
    }
    response = client.post(
        "/feedback",
        json=feedback_data
    )
    assert response.status_code == 200
    return response

# Test for feedback insertion
def test_create_feedback():
    lab_id = create_new_lab().json()
    response = create_feedback(lab_id)
    feedback_id = response.json()

    # QUery db and check for insertion
    with TestingSessionLocal() as mock_db:
        db_feedback = mock_db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
        assert db_feedback and db_feedback.id == feedback_id

# Test for get feedback 
def test_get_all_feedback():
    lab_id = create_new_lab().json()

    # Create 10 feedback    
    for _ in range(10):
        create_feedback(lab_id)

    
    # Query api and check for insertion
    response = client.get("/feedback/{0}".format(lab_id))
    assert response.status_code == 200
    assert len(response.json()) == 10


# Test for delete feedback by labid
def test_delete_feedback_by_lab_id():
    lab_id = create_new_lab().json()

    # Create 10 feedback    
    for _ in range(10):
        create_feedback(lab_id)

    # Query api and check for insertion
    response = client.delete("/feedback/{0}".format(lab_id))
    assert response.status_code == 200

    # Query api and check for insertion
    response = client.get("/feedback/{0}".format(lab_id))
    assert response.status_code == 200
    assert len(response.json()) == 0


# Unit test for uploading a file
def test_upload_file_to_filestorage():
    # Create a new lab helper function
    response = create_new_lab()

    lab_id = response.json()
    assert response.status_code == 200

    # Upload a file
    with open("tests/test_other.py", "rb") as file:
        response = client.post(
            "/uploadfile",
            files={"file": ("test_file.txt", file, "text/plain")}
        )
        assert response.status_code == 200
        #assert response.url.contains("https://rle-filestorage.s3.amazonaws.com/")
    
    #TODO: Add test for file storage exsitence
     