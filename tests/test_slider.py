import models
from tests.base import *
from fastapi.encoders import jsonable_encoder

def create_new_slider_image(lab_id:int,auth_cookie):
    slider_data = {
        "lab_id": lab_id,
        "slider_image": "string"
    }
    
    client.cookies.set(COOKIE_KEY, auth_cookie)

    response = client.post(
        "/sliderimage",
        json=slider_data
    )

    return response

# Unit test for slider image insertion
def test_create_slider_image():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    sli_response = create_new_slider_image(lab_id,authorized_jwt_token_admin)
    
    # Check for status code
    assert sli_response.status_code == 200
    
    slider_id = sli_response.json()
    
    # Query mock db for publication insertion
    with TestingSessionLocal() as mock_db:
        slider = mock_db.query(models.Slider).filter(models.Slider.id == slider_id).first()
        assert slider and slider.id == slider_id

# Unit test for slider image update 
def test_update_slider_image():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    sli_response = create_new_slider_image(lab_id,authorized_jwt_token_admin)
    
    # Check for status code
    assert sli_response.status_code == 200
    
    slider_id = sli_response.json()
    
    with TestingSessionLocal() as mock_db:
        slider = mock_db.query(models.Slider).filter(models.Slider.id == slider_id).first()
        slider.lab_id = lab_id
        slider.slider_binary_id = slider.slider_binary_id
        
        response = client.put(
            "/sliderimage/{0}".format(slider_id),
            json = jsonable_encoder(slider)
        )
        assert response.status_code == 200
        
        updated_sli = mock_db.query(models.Slider).filter(models.Slider.id == slider_id).first()
        
        assert slider.lab_id == updated_sli.lab_id
        assert slider.slider_binary_id == updated_sli.slider_binary_id
        

def test_delete_slider_image():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    sli_response = create_new_slider_image(lab_id,authorized_jwt_token_admin)
    
    # Check for status code
    assert sli_response.status_code == 200
    
    slider_id = sli_response.json()
    
    response = client.delete(
        "/slider?slider_id={0}".format(slider_id)
    )
    assert response.status_code == 200
    
    with TestingSessionLocal() as mock_db:
        slider = mock_db.query(models.Slider).filter(models.Slider.id == slider_id).first()
        assert slider is None


def test_create_slider_access_levels():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    # Create a new slider image unauthorized
    sli_response = create_new_slider_image(lab_id,unauthorized_jwt_token)
    assert sli_response.status_code == 401
    
    # Create a new slider by user of same lab
    cookie = create_auth_token("user",lab_id)
    slider_response = create_new_slider_image(lab_id,cookie)
    assert slider_response.status_code == 200
    
    # Create a new slider by user of different lab
    #cookie = create_auth_token("user",lab_id-1)
    #slider_response = create_new_slider_image(lab_id,cookie)
    #assert pub_response.status_code == 401
    
    # Create a new slider by manager of same lab
    cookie = create_auth_token("manager",lab_id)
    slider_response = create_new_slider_image(lab_id,cookie)
    assert slider_response.status_code == 200
    
    # Create a new slider by manager of different lab
    #cookie = create_auth_token("manager",lab_id-1)
    #slider_response = create_new_slider(lab_id,cookie)
    #assert slider_response.status_code == 401


def test_update_slider_access_levels():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    sli_response = create_new_slider_image(lab_id,authorized_jwt_token_admin)
    
    # Check for status code
    assert sli_response.status_code == 200
    
    slider_id = sli_response.json()
    
    with TestingSessionLocal() as mock_db:
        slider = mock_db.query(models.Slider).filter(models.Slider.id == slider_id).first()
        assert slider is not None
        
        #Unauthorized
        client.cookies.set(COOKIE_KEY, unauthorized_jwt_token)
        response = client.put(
            "/sliderimage/{0}".format(slider_id),
            json = jsonable_encoder(slider)
        ) 
        assert response.status_code == 401
        
        # Update by user of same lab
        cookie = create_auth_token("user",lab_id)
        client.cookies.set(COOKIE_KEY, cookie)
        response = client.put(
            "/sliderimage/{0}".format(slider_id),
            json = jsonable_encoder(slider)
        ) 
        assert response.status_code == 200
        
        # Update by user of different lab
        #cookie = create_auth_token("user",lab_id-1)
        #client.cookies.set(COOKIE_KEY, cookie)
        #response = client.put(
        #    "/sliderimage/{0}".format(slider_id),
        #    json = jsonable_encoder(slider)
        #) 
        #assert response.status_code == 401
        
        # Update by manager of same lab
        cookie = create_auth_token("manager",lab_id)
        client.cookies.set(COOKIE_KEY, cookie)
        response = client.put(
            "/sliderimage/{0}".format(slider_id),
            json = jsonable_encoder(slider)
        ) 
        assert response.status_code == 200
        
        # Update by manager of different lab
        #cookie = create_auth_token("manager",lab_id-1)
        #client.cookies.set(COOKIE_KEY, cookie)
        #response = client.put(
        #    "/sliderimage/{0}".format(slider_id),
        #    json = jsonable_encoder(slider)
        #) 
        #assert response.status_code == 401 


def test_delete_slider_access_levels():
    lab_response = create_new_lab()
    
    # Check for status code
    assert lab_response.status_code == 200
    
    lab_id = lab_response.json()
    
    sli_response = create_new_slider_image(lab_id,authorized_jwt_token_admin)
    
    # Check for status code
    assert sli_response.status_code == 200
    
    slider_id = sli_response.json()
    
    # Unauthorized
    client.cookies.set(COOKIE_KEY, unauthorized_jwt_token)
    response = client.delete(
        "/slider?slider_id={0}".format(slider_id)
    )
    assert response.status_code == 401
    
    # Delete by manager of different lab
    #cookie = create_auth_token("manager",lab_id-1)
    #client.cookies.set(COOKIE_KEY, cookie)
    #response = client.delete(
    #    "/slider?slider_id={0}".format(slider_id)
    #)
    #assert response.status_code == 401 
    
    # Delete by manager of same lab
    cookie = create_auth_token("manager",lab_id)
    client.cookies.set(COOKIE_KEY, cookie)
    response = client.delete(
        "/slider?slider_id={0}".format(slider_id)
    )
    assert response.status_code == 200               
           
    