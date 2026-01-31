import os
import arel
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.database import Base, engine
from app.routes import auth

templates = Jinja2Templates(directory="app/templates")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI SaaS Starter")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
    
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
def show_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def show_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})