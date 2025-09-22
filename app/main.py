from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import RequestValidationError as FastAPIRequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import users_controller, auth_controller, insurance_controller, email_controller, members_controller
from app.config.database import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="myFolio API")

# Routers
app.include_router(users_controller.router)
app.include_router(auth_controller.router)
app.include_router(insurance_controller.router)
app.include_router(email_controller.router)
app.include_router(members_controller.router)

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

# Global error handler to always return JSON (and CORS headers)
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers={"Access-Control-Allow-Origin": origins[0]}  # or use "*" if you want
    )

@app.exception_handler(FastAPIRequestValidationError)
async def validation_exception_handler(request: Request, exc: FastAPIRequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
        headers={"Access-Control-Allow-Origin": origins[0]}
    )