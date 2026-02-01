from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.database import Base, engine
from app.routes.auth import router, get_current_user
from app.models.user import User

templates = Jinja2Templates(directory="app/templates")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI SaaS Starter")

app.include_router(router, prefix="/auth", tags=["auth"])
    
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, user: User = Depends(get_current_user)):
    if user:
        return RedirectResponse(url="/dashboard", status_code=303)
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
def show_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/reset-password", response_class=HTMLResponse)
def show_reset(request: Request):
    return templates.TemplateResponse("reset_password.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def show_login(request: Request, user: User = Depends(get_current_user)):
     # If the gatekeeper didn't find a user, kick them to login
    if user:
        return RedirectResponse(url="/dashboard", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard")
async def dashboard(request: Request, user: User = Depends(get_current_user)):
    # If the gatekeeper didn't find a user, kick them to login
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    # Now you can pass the 'user' object directly to your template!
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "user": user
    })