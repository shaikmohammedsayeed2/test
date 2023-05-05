This is the file for adding back end protocols for swe project where we are building the python based api using fastapi

## Setup 

``` pip install "fastapi[all]" sqlalchemy azure-storage-blob psycopg2 google-oauth2-tool pyjwt python-jose[cryptography] google-auth google-auth-oauthlib google-auth-httplib2``` 

## Run
``` uvicorn main:app --reload ```

## Test
Swagger UI: ```GET {HOST_URL}/docs```




