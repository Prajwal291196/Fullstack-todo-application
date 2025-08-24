from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta

from app.auth.jwt_handler import create_access_token, get_current_user, fake_user, Token
from app.routes.todos import router as todo_router
from config.settings import settings

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

# Login route
@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != fake_user["email"] or form_data.password != fake_user["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": fake_user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Protected example route
# @app.get("/protected")
# def protected_route(user: dict = Depends(get_current_user)):
#     return {"message": f"Hello {user['email']}, you accessed a protected route!"}

# ✅ Register todo routes
app.include_router(todo_router)
