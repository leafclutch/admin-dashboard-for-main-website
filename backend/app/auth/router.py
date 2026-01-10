from fastapi import APIRouter, HTTPException, Depends # Tools to build the API
from app.auth.schemas import LoginRequest, TokenResponse
from app.utils.jwt import create_access_token

from app.utils.security import verify_password # password verification function
from app.db.session import get_db # database session
from sqlalchemy.orm import session
from app.models.login_model import AdminUser
from app.auth.deps import get_current_user

# Setup the router for Login and User info
router = APIRouter(prefix="/auth", tags=["Auth"])

# 1. Login to get a token
@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: session = Depends(get_db)):
    # Step 1: Look for the user in the database by their email
    user = db.query(AdminUser).filter(AdminUser.email==data.email).first()

    # Step 2: If the user doesn't exist, stop and show an error
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Step 3: Check if the password is correct
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Step 4: If everything is correct, create a secure login token
    token = create_access_token({
        "sub": user.email,
        "role": "admin"
    })

    # Step 5: Send the token back to the user
    return {"access_token": token}

# 2. Get the details of the logged-in user
@router.get("/me")
def get_me(current_user: AdminUser = Depends(get_current_user)):
    return{
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active,
    }
