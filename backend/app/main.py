from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.routes.db_health import router as health_router
from app.routes import training
from app.routes import mentors


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
app.include_router(health_router)


@app.get("/")
def health():
    return {"status": "ok"}


