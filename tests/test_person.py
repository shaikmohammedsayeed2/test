import models
from tests.base import *
from fastapi.encoders import jsonable_encoder
from session import COOKIE_KEY



def create_person(lab_id, auth_cookie):
    person_data = {
        "name": "string",
        "roll_number": "string",
        "linkedin_url": "string",
        "github_url": "string",
        "personal_web_url": "string",
        "lab_id": int(lab_id),
        "person_role": "student",
        "user_role": "admin",
        "person_image": "string"
    }

    client.cookies.set(COOKIE_KEY, auth_cookie)

    response = client.post("/person", json=person_data)
    return response



# Unit test for person retrieval
def test_get_person():
    # Create a new lab 
    response = create_new_lab()
    # Check for status code 
    assert response.status_code == 200
    lab_id = response.json()
    
    # Create a new person from helper function
    response = create_person(lab_id, authorized_jwt_token_admin)
    assert response.status_code == 200

    person_id = response.json()
    
    # Check the person get api
    response = client.get("/person/{0}".format(person_id))
    assert response.status_code == 200


# Unit test for person insertion
def test_create_person():
    # Create a new lab 
    response = create_new_lab()
    # Check for status code 
    assert response.status_code == 200
    lab_id = response.json()
    
    # Create a new person from helper function
    response = create_person(lab_id, authorized_jwt_token_admin)
    assert response.status_code == 200

    person_id = response.json()
    
    # Query mock db for person insertion
    with TestingSessionLocal() as mock_db:
        person = mock_db.query(models.Person).filter(models.Person.id == person_id).first()
        assert person and person.id == person_id




# Unit test for person update
def test_update_person():
    # Create a new lab 
    response = create_new_lab()
    # Check for status code 
    assert response.status_code == 200
    lab_id = response.json()
    
    # Create a new person from helper function
    response = create_person(lab_id, authorized_jwt_token_admin)
    assert response.status_code == 200

    person_id = response.json()
    
    # Query mock db for person insertion
    with TestingSessionLocal() as mock_db:
        person = mock_db.query(models.Person).filter(models.Person.id == person_id).first()
        person.name = "Updated name"
        person.roll_number = "Updated roll_number"
        person.linkedin_url = "Updated linkedin_url"
        person.github_url = "Updated github_url"
        person.personal_web_url = "Updated personal_web_url"
        person.lab_id = lab_id
        person.person_role = "faculty"
        person.user_role = "manager"
        person.person_image = "Updated person_image"

        client.cookies.set(COOKIE_KEY, authorized_jwt_token_admin)

        # Update using the Update API
        response = client.put(
            "/person/{0}".format(person_id),
            json=jsonable_encoder(person)
        )
        assert response.status_code == 200

        # Query mock db for lab updation
        n_person = mock_db.query(models.Person).filter(models.Person.id == person_id).first()

        assert person.name == n_person.name
        assert person.roll_number == n_person.roll_number
        assert person.linkedin_url == n_person.linkedin_url
        assert person.github_url == n_person.github_url
        assert person.personal_web_url == n_person.personal_web_url
        assert person.lab_id == n_person.lab_id
        assert person.person_role == n_person.person_role
        assert person.user_role == n_person.user_role
        assert person.person_image == n_person.person_image

    
        # Test is done



# Unit test for person deletion
def test_delete_person():
    # Create a new lab 
    response = create_new_lab()
    # Check for status code 
    assert response.status_code == 200
    lab_id = response.json()
    
    # Create a new person from helper function
    response = create_person(lab_id, authorized_jwt_token_admin)
    assert response.status_code == 200

    person_id = response.json()
    
    # Get lab_member id from db
    with TestingSessionLocal() as mock_db:
        lab_member = mock_db.query(models.LabMember).filter(models.LabMember.person_id == person_id).first()
        assert lab_member is not None

        client.cookies.set(COOKIE_KEY, authorized_jwt_token_admin)

        # Delete using the Delete API
        response = client.delete(
            "/person?labmember_id={0}".format(lab_member.id)
        )
        assert response.status_code == 200

        # Query mock db for person deletion
        person = mock_db.query(models.Person).filter(models.Person.id == person_id).first()
        assert person is None


# Unit test for Person Create without neccesary access
def test_create_person_access_levels():
    # Create a new lab 
    response = create_new_lab()
    # Check for status code 
    assert response.status_code == 200
    lab_id = response.json()
    
    # Create a new person Unauthorized
    response = create_person(lab_id, unauthorized_jwt_token)
    assert response.status_code == 401

    # Create a new person by manager of same lab
    cookie = create_auth_token("manager",lab_id)
    response = create_person(lab_id, cookie)
    assert response.status_code == 200

    # Create a new person by manager of different lab
    cookie = create_auth_token("manager",lab_id-1)
    response = create_person(lab_id, cookie)
    assert response.status_code == 401

    # Create a new person User
    response = create_person(lab_id, authorized_jwt_token_user)
    assert response.status_code == 401



# Unit test for Person Update without neccesary access
def test_update_person_access_levels():
    # Create a new lab 
    response = create_new_lab()
    # Check for status code 
    assert response.status_code == 200
    lab_id = response.json()
    
    # Create a new person from helper function
    response = create_person(lab_id, authorized_jwt_token_admin)
    assert response.status_code == 200

    person_id = response.json()
    
    # Get lab_member id from db
    with TestingSessionLocal() as mock_db:
        person = mock_db.query(models.Person).filter(models.Person.id == person_id).first()
        assert person is not None

        # Unauthorized
        client.cookies.set(COOKIE_KEY, unauthorized_jwt_token)
        response = client.put("/person/{0}".format(person_id),json=jsonable_encoder(person))
        assert response.status_code == 401

        # Update person by: manager of same lab
        cookie = create_auth_token("manager",lab_id)
        client.cookies.set(COOKIE_KEY, cookie)
        response = client.put("/person/{0}".format(person_id),json=jsonable_encoder(person))
        assert response.status_code == 200

        # Update person by: manager of different lab
        cookie = create_auth_token("manager",lab_id-1)
        client.cookies.set(COOKIE_KEY, cookie)
        response = client.put("/person/{0}".format(person_id),json=jsonable_encoder(person))
        assert response.status_code == 401

        # Update by diffrent User 
        cookie = create_auth_token("user",lab_id,person_id-1)
        client.cookies.set(COOKIE_KEY, cookie)
        response = client.put("/person/{0}".format(person_id),json=jsonable_encoder(person))
        assert response.status_code == 401

        # Update by self
        cookie = create_auth_token("user",lab_id, person_id)
        client.cookies.set(COOKIE_KEY, cookie)
        response = client.put("/person/{0}".format(person_id),json=jsonable_encoder(person))
        assert response.status_code == 200


# Unit test for Person Delete without neccesary access
def test_delete_person_access_levels():
    # Create a new lab 
    response = create_new_lab()
    # Check for status code 
    assert response.status_code == 200
    lab_id = response.json()
    
    # Create a new person from helper function
    response = create_person(lab_id, authorized_jwt_token_admin)
    assert response.status_code == 200

    person_id = response.json()
    
    # Get lab_member id from db
    with TestingSessionLocal() as mock_db:
        lab_member = mock_db.query(models.LabMember).filter(models.LabMember.person_id == person_id).first()
        assert lab_member is not None

        # Unauthorized
        client.cookies.set(COOKIE_KEY, unauthorized_jwt_token)
        response = client.delete("/person?labmember_id={0}".format(lab_member.id))
        assert response.status_code == 401

        # Delete person by: manager of same lab
        cookie = create_auth_token("manager",lab_id)
        client.cookies.set(COOKIE_KEY, cookie)
        response = client.delete("/person?labmember_id={0}".format(lab_member.id))
        assert response.status_code == 200

        # Update person by: manager of different lab
        cookie = create_auth_token("manager",lab_id-1)
        client.cookies.set(COOKIE_KEY, cookie)
        response = client.delete("/person?labmember_id={0}".format(lab_member.id))
        assert response.status_code == 401

        # Update by diffrent User 
        cookie = create_auth_token("user",lab_id,person_id-1)
        client.cookies.set(COOKIE_KEY, cookie)
        response = client.delete("/person?labmember_id={0}".format(lab_member.id))
        assert response.status_code == 401

        # Update by self
        cookie = create_auth_token("user",lab_id, person_id)
        client.cookies.set(COOKIE_KEY, cookie)
        response = client.delete("/person?labmember_id={0}".format(lab_member.id))
        assert response.status_code == 200