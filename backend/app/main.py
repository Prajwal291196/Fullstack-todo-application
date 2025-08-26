from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta

from app.auth.jwt_handler import create_access_token, get_current_user, fake_user, Token
from app.routes.todos import router as todo_router
from config.settings import settings

from sqlalchemy.orm import Session
from .auth.jwt_handler import get_password_hash, verify_password
from .models.users import User
from .database.database import get_db
from .schemas import user

app = FastAPI()

# Allow CORS
origins = [
    "http://localhost:5173",   # React dev server
    "http://127.0.0.1:5173"    # Some setups use 127.0.0.1 instead
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # allow these domains
    allow_credentials=True,
    allow_methods=["*"],       # allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],       # allow all headers
)

# Register user
# @app.post("/register")
# def register(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.username == user.username).first()
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username already registered")
#     hashed_pw = get_password_hash(user.password)
#     new_user = User(username=user.username, hashed_password=hashed_pw)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return {"msg": "User created successfully"}

@app.post("/register")
def register_user(user: user.UserCreate, db: Session = Depends(get_db)):
    # Check if username/email already exists
    try:
        # check if user exists
        db_user = db.query(User).filter(User.username == user.username).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        hashed_password = get_password_hash(user.password)
        new_user = User(username=user.username, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except Exception as e:
        print("❌ Error in register:", e)
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@app.post("/login", response_model=Token)
def login(user: user.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            # headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# # Login route
# @app.post("/login", response_model=Token)
# def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     if form_data.username != fake_user["email"] or form_data.password != fake_user["password"]:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": fake_user["email"]}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


# Protected example route
# @app.get("/protected")
# def protected_route(user: dict = Depends(get_current_user)):
#     return {"message": f"Hello {user['email']}, you accessed a protected route!"}

# ✅ Register todo routes
app.include_router(todo_router)
