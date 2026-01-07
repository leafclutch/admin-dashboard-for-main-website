from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.routes.db_health import router as health_router
from app.routes import training
from app.routes import mentors
from app.routes import services
from app.routes import service_tech, service_offering
from app.routes import members
from app.routes import projects
from app.routes import project_feedback
from app.routes import opportunities


load_dotenv()

app = FastAPI(title="Leafclutch backend")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(training.router)
app.include_router(mentors.router)
app.include_router(services.router)
app.include_router(service_tech.router)
app.include_router(service_offering.router)
app.include_router(members.router)
app.include_router(projects.router)
app.include_router(project_feedback.router)
app.include_router(opportunities.router)
app.include_router(health_router)


@app.get("/")
def health():
    return {"status": "ok"}


