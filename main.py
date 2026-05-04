from fastapi import HTTPException
from fastapi import FastAPI, Depends 
from sqlalchemy.orm import Session

import models, schemas, crud
from database import engine, SessionLocal, Base

from auth import verify_password, create_token
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from auth import verify_password

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db   #Send this database connection to the API function
    finally:
        db.close()


# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"

# Register API
@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

# Login API
@app.post("/login")
def login(user: schemas.Login, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)

    if not db_user:
        raise HTTPException(status_code=401, detail="User not found")

    is_valid = verify_password(user.password, db_user.password)

    print("VERIFY RESULT:", is_valid)

    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

# Get current user
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")
    return email

# Protected route
@app.get("/profile")
def profile(user: str = Depends(get_current_user)):
    return {"logged_in_user": user}



# CREATE
@app.post("/users/", response_model=schemas.UserResponse)
def create(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

# READ ALL
@app.get("/users/")
def read_all(db: Session = Depends(get_db)):
    return crud.get_users(db)

# READ ONE
@app.get("/users/{user_id}")
def read_one(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id)

# UPDATE
@app.put("/users/{user_id}")
def update(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.update_user(db, user_id, user)

# DELETE
@app.delete("/users/{user_id}")
def delete(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id)