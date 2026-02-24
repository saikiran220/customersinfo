from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from supabase import create_client, Client
import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Load .env from backend directory
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="User Data Entry API")

# CORS - configurable via CORS_ORIGINS env (e.g. "*" for dev or "https://myapp.com" for production)
# When unset: allow any localhost port (for Vite dev server). For production, set CORS_ORIGINS to your frontend URL.
_cors_origins = os.getenv("CORS_ORIGINS", "").strip()
if _cors_origins == "*":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
elif _cors_origins:
    _origins = [o.strip() for o in _cors_origins.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    # Allow any localhost / 127.0.0.1 port (covers Vite dev ports like 5173, 32770, etc.)
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
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


@app.get("/health")
def health():
    """Check Supabase connectivity and table access. Helps debug 500s."""
    try:
        supabase = get_supabase()
        # Simple query to verify table exists and we have permission
        r = supabase.table("users").select("id").limit(1).execute()
        return {"status": "ok", "database": "reachable", "table": "users"}
    except HTTPException:
        raise
    except Exception as e:
        log.exception("Health check failed: %s", e)
        return {
            "status": "error",
            "database": "unreachable or misconfigured",
            "hint": _friendly_error_message(e),
        }


def _friendly_error_message(e: Exception) -> str:
    """Turn backend/Supabase errors into user-friendly messages."""
    raw = str(e)
    # PostgREST/Supabase APIError has .message and .details
    if hasattr(e, "message") and getattr(e, "message", None):
        raw = str(e.message) or raw
    if hasattr(e, "details") and getattr(e, "details", None):
        raw = str(e.details) if not raw else raw

    msg = raw.lower() if raw else ""

    # Try to parse Supabase/PostgREST JSON error (e.g. '{"message":"...","code":"..."}')
    if raw and raw.strip().startswith("{"):
        try:
            obj = json.loads(raw)
            if isinstance(obj, dict) and obj.get("message"):
                raw = obj["message"]
                msg = raw.lower()
        except Exception:
            pass

    if "relation" in msg and "does not exist" in msg:
        return (
            "Database table 'users' does not exist. "
            "Run the SQL in backend/supabase_schema.sql in your Supabase project (SQL Editor)."
        )
    if "permission denied" in msg or "policy" in msg or "row level security" in msg or "rls" in msg:
        return (
            "Database permission denied. "
            "Ensure the 'users' table has RLS policies allowing insert (see backend/supabase_schema.sql)."
        )
    if "invalid" in msg and "key" in msg:
        return "Invalid Supabase API key. Check SUPABASE_ANON_KEY in backend/.env"
    if "connection" in msg or "timeout" in msg or "10060" in msg:
        return "Cannot reach the database. Check your internet, firewall, or VPN and try again."
    if "jwt" in msg or "expired" in msg or "unauthorized" in msg or "invalid api key" in msg:
        return "Invalid or expired Supabase API key. Check SUPABASE_ANON_KEY in backend/.env (Supabase → Settings → API)."
    return raw if raw else "An unexpected error occurred. Check backend logs."


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
    except (OSError, ConnectionError, TimeoutError):
        raise HTTPException(
            status_code=503,
            detail="Cannot reach the database. Check your internet, firewall, or VPN and try again.",
        )
    except HTTPException:
        raise
    except Exception as e:
        log.exception("POST /users failed: %s", e)
        detail = _friendly_error_message(e)
        raise HTTPException(status_code=500, detail=detail)
