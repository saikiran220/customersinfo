from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from supabase import create_client, Client
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from backend directory
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="User Data Entry API")

# CORS - configurable via CORS_ORIGINS env (e.g. "*" for dev or "https://myapp.com" for production)
# For production, use a specific frontend URL, not "*"
_cors_origins = os.getenv("CORS_ORIGINS", "").strip()
if _cors_origins == "*":
    _origins = ["*"]
elif _cors_origins:
    _origins = [o.strip() for o in _cors_origins.split(",") if o.strip()]
else:
    _origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:32769",
        "http://127.0.0.1:32769",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, description="User's name")
    father_name: str = Field(..., min_length=1, description="Father's name")
    mobile_no: str = Field(..., pattern=r"^\d{10}$", description="10 digit mobile number")


def get_supabase() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise HTTPException(
            status_code=500,
            detail="Supabase URL and API key must be set in .env file",
        )
    return create_client(url, key)


@app.get("/")
def root():
    return {"message": "User Data Entry API is running"}


@app.post("/users")
def create_user(user: UserCreate):
    try:
        supabase = get_supabase()
        data = {
            "name": user.name,
            "father_name": user.father_name,
            "mobile_no": user.mobile_no,
        }
        result = supabase.table("users").insert(data).execute()
        return {"message": "User created successfully", "data": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
