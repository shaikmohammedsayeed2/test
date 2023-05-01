from fastapi import HTTPException, Request
import jwt
import models
from sqlalchemy.orm import Session

# Google OAuth2 client ID
CLIENT_ID = '658208509868-eobuvr8pnb5k1knq91cq27tl794rp67l.apps.googleusercontent.com'
GSUITE_DOMAIN_NAME = "iith.ac.in"
JWT_SCERET = "68a89b238f114ec7b4dbe1d69014399ff18ec2b22f12146fd63a98faf398d80f"
COOKIE_KEY = "rle_session"



class RleSession:
    
    def __init__(self, jwt_payload, noSession = False):
        if noSession:
            self.valid = noSession
            self.reason = jwt_payload
        
        self.setFields(jwt_payload['userid'],
                jwt_payload['name'], 
                jwt_payload['email'],
                jwt_payload['role_id'], 
                jwt_payload['person_id'], 
                jwt_payload['role_name']
                )

    def setFields(self, user_id, name, email, role_id, person_id, role_name):
        self.userid = user_id
        self.name =  name
        self.email = email
        self.role_id = role_id
        self.person_id = person_id
        self.role_name = role_name
        self.valid = True

    
        
    def __str__(self) -> str:
        if not self.valid:
            return str({"valid":self.valid,"reason":self.reason})
        else:
            return str({
                "email":self.email,
                "name":self.name,
                "valid":self.valid,
                "role_id":self.role_id
                })

# This function verifies the JWT token and returns the decoded payload
def get_rle_session(request: Request):
    ## Remove this to validate api
    rle_session_ck = request.cookies.get(COOKIE_KEY)
    if not rle_session_ck:
        return RleSession("No Cookie",noSession=True)
    try:
        decoded_token = jwt.decode(rle_session_ck, JWT_SCERET,algorithms="HS256")
        return RleSession(decoded_token)
    
    except (jwt.exceptions.InvalidTokenError, jwt.exceptions.InvalidSignatureError,ValueError, KeyError) as v:
        print(v.with_traceback())
        return RleSession("Invalid Token",noSession=True)
    
 



def get_person_role_by_email(email:str,lab_id:int,db:Session):
    # get person id from email
    person = db.query(models.Person).filter(models.Person.roll_number == email).first()
    # print(person)
    if not person:
        raise HTTPException(status_code=401, detail='User not authorized for this lab')
    lab_member = db.query(models.LabMember).filter(models.LabMember.person_id == person.id,models.LabMember.lab_id==lab_id).first()
    if not lab_member:
        raise HTTPException(status_code=401, detail='User not authorized for this lab')
    
    return lab_member.role_id,lab_member.person_id
    
