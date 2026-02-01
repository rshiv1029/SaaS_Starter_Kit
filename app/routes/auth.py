from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.database import get_db
from app.models.user import User
from app.utils.security import create_access_token, hash_password, verify_password
from app.config import settings

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        full_name=user.full_name,
        credits=1000
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User created successfully", "email": new_user.email}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {
        "message": "Login successful",
        "user": {
            "email": db_user.email,
            "full_name": db_user.full_name,
            "credits": db_user.credits
        }
    }

@router.get("/register-page", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register-page")
def register_page_submit(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        request.session['error'] = "Email already registered"
        return RedirectResponse(url="/register", status_code=303)
    
    new_user = User(
        email=email,
        hashed_password=hash_password(password),
        full_name=full_name,
        credits=1000
    )
    db.add(new_user)
    db.commit()
    
    request.session['success'] = "Account created successfully! Please login."
    
    # Explicitly clear any auth cookies to prevent auto-login
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("access_token")
    return response

@router.get("/login-page", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login-page")
def login_page_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        request.session['error'] = "Invalid email or password"
        return RedirectResponse(url="/login", status_code=303)
    
    # Generate JWT token
    token = create_access_token(data={"sub": user.email})
    max_age_seconds = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(
        key="access_token", 
        value=f"Bearer {token}", 
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax",
        max_age=max_age_seconds
    )
    return response


@router.get("/reset-password", response_class=HTMLResponse)
def reset_password_page(request: Request):
    return templates.TemplateResponse("reset-password.html", {"request": request})

@router.post("/reset-password-page")
def reset_password_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    confirmedPassword: str = Form(...),
    db: Session = Depends(get_db)
):
    # TODO: Add email verification with reset token
    # Current implementation is for development only
    
    # Password validation
    if password != confirmedPassword:
        request.session['error'] = "Passwords do not match"
        return RedirectResponse(url="/reset-password", status_code=303)

    # Find the existing user
    user = db.query(User).filter(User.email == email).first()
    
    # If user doesn't exist, handle the error
    if not user:
        request.session['error'] = "No account found with this email"
        return RedirectResponse(url="/reset-password", status_code=303)
    
    # 4. Update the existing user's password
    # We use security.hash_password (ensure you have it imported)
    user.hashed_password = hash_password(password)
    
    # 5. Commit the changes to the database
    db.commit()
    
    # 6. Redirect to login with a success message (if your login template handles it)
    request.session['success'] = "Password reset successful! You can now login."
    return RedirectResponse(url="/login", status_code=303)

@router.get("/logout")
async def logout(request: Request):
    request.session['info'] = "You have been logged out successfully"
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response

def get_current_user(request: Request, db: Session = Depends(get_db)):
    # Get token from cookie
    token = request.cookies.get("access_token")
    if not token:
        return None # Or raise HTTPException to redirect to login
    try:
        # Decode token and remove 'Bearer ' prefix
        scheme, _, param = token.partition(" ")
        print(f"DEBUG: Checking token for user. Token exists: {bool(param)}")
        payload = jwt.decode(param, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        user = db.query(User).filter(User.email == email).first()
        print(f"DEBUG: User found: {user.email if user else None}")
        return user
    except JWTError as e:
        print(f"DEBUG: JWT Error: {e}")
        return None