from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserBase

router = APIRouter()

# OAuth2PasswordBearer is the token URL for login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/register")
def register(name: str, email: str, password: str):
  #Register a new user.
  if email in fake_users_db:
    raise HTTPException(status_code=400, detail="Email is already registered")
  hashed_password = hash_password(password)
  fake_users_db[email] = {"name": name, "email": email, "hashed_password": hashed_password}
  return {"message": "User registered successfully!"}


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    #Login and return a JWT token.
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["email"]}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    #A protected route requiring a valid JWT.
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    email = payload.get("sub")
    return {"message": f"Hello, {email}!"}