from fastapi import Depends, HTTPException, APIRouter, Response
from google.oauth2 import id_token
from google.auth.exceptions import InvalidValue
import jwt
import schemas, utils
from sqlalchemy.orm import Session

from google.oauth2 import id_token
from google.auth.transport import requests
from session import *


router = APIRouter()

@router.post("/auth/signin")
async def after_sign_in(signin_data:schemas.SignInData, response:Response, db: Session = Depends(utils.get_session)):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(signin_data.g_token, requests.Request(), CLIENT_ID)

        # If auth request is from a G Suite domain:
        if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            raise ValueError('Wrong hosted domain.')

        role_id,person_id = get_person_role_by_email(idinfo['email'],signin_data.lab_id,db);
        # ID token is valid. Get the user's Google Account ID from the decoded token.
        jwt_payload = {
            "userid" : idinfo['sub'],
            "name":idinfo['name'],
            "email":idinfo['email'],
            "role_id": role_id,
            "person_id": person_id,
            "role_name":utils.get_role_name_by_id(role_id)
            }
        # Creating a JWT and send cookie
        jwt_token = jwt.encode(jwt_payload,JWT_SCERET,algorithm="HS256")
        response.set_cookie(COOKIE_KEY, jwt_token,samesite="lax")

        return jwt_payload
    

    # except ValueError as v:
    #     # Invalid token
    #     print(v.with_traceback())

    except InvalidValue:
        return HTTPException(status_code=401, detail='Token is invalid')
    
