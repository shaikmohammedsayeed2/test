from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from api import events,home,images,lab,other,people,research
import uvicorn

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

# Include routers
app.include_router(home.router,tags=["Home"])
app.include_router(lab.router, tags=["Lab"])
app.include_router(people.router, tags=["Person"])
app.include_router(research.router, tags=["Research"])
app.include_router(events.router, tags=["Events"])
app.include_router(images.router, tags=["Images"])
app.include_router(other.router, tags=["Other"])


#Redirection to the docs [Only for debug]
@app.get("/")
def redirect():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
