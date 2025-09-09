from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import users_controller, auth_controller, insurance_controller, email_controller
from app.config.database import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="myFolio API")

# Routers
app.include_router(users_controller.router)
app.include_router(auth_controller.router)
app.include_router(insurance_controller.router)
app.include_router(email_controller.router)

# CORS
origins = [
    "http://localhost:4200",
    "https://myfolio.catalytix.in"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)