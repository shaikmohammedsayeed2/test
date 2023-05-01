from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api import events,home,images,lab,other,people,research
import session
import uvicorn
from session import check_access_level
from fastapi.responses import JSONResponse, RedirectResponse


tags_metadata = [
    {
        "name": "Home",
        "description": "APIs related to home page",
    },
    {
        "name": "Lab",
        "description": "APIs related to Lab ",
    },
    {
        "name": "Person",
        "description": "APIs related to people",
    },
    {
        "name": "Images",
        "description": "APIs related to Images like sliders, gallery",
    },
    {
        "name": "Events",
        "description": "APIs related to events",
    },
    {
        "name": "Research",
        "description": "Publications, Posterdemos, Patent",
    },
    {
        "name": "Other"
    },
    {
        "name":"Auth"
    }
]


app = FastAPI(openapi_tags=tags_metadata)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Middleware to check access to CUD operations
@app.middleware("http")
async def check_access(request: Request, call_next):
    # This middleware executes non GET requests
    # Optoins request is sent by browser to check if the server is CORS enabled
    # So, we need to allow it
    if request.method not in ["GET","OPTIONS"] and  request.url.path != "/auth/signin" : 

        ret = check_access_level(request.cookies)
        if ret != True:
            #print(ret,"Cookies:",request.cookies,"Cookies end")
            return JSONResponse(status_code=401,content={'reason': "Unauthorized access"})
        

    response = await call_next(request)
    return response


# Include routers
app.include_router(home.router,tags=["Home"])
app.include_router(lab.router, tags=["Lab"])
app.include_router(people.router, tags=["Person"])
app.include_router(research.router, tags=["Research"])
app.include_router(events.router, tags=["Events"])
app.include_router(images.router, tags=["Images"])
app.include_router(other.router, tags=["Other"])
app.include_router(session.router, tags=["Auth"])


# Redirection to the docs [Only for debug]
@app.get("/")
def redirect():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
