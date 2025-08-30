from fastapi import FastAPI
from app.controllers import users_controller, auth_controller
from app.config.database import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="myFolio API")

# Routers
app.include_router(users_controller.router)
app.include_router(auth_controller.router)