
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.database import check_database_connection
from app.email_service import (
    save_email,
    get_all_emails,
    get_email_by_id
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting MailMind Backend...")

    if check_database_connection():
        print("MongoDB is ready!")
    else:
        print("Warning: MongoDB connection failed!")

    yield

    print("MailMind Backend Stopped.")


app = FastAPI(
    title="MailMind - AI Email Assistant",
    description="AI-powered email summarization and prioritization.",
    version="1.0.0",
    lifespan=lifespan
)


# Email request model
class EmailCreate(BaseModel):
    gmail_message_id: str
    sender: str
    subject: str
    received_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    summary: str = ""
    priority: str = "Medium"
    action_items: list[str] = Field(default_factory=list)
    is_unread: bool = True


@app.get("/")
def home():
    return {
        "message": "Welcome to MailMind!",
        "project": "AI Email Assistant",
        "status": "running"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "message": "MailMind backend is working!"
    }


@app.get("/api/database-status")
def database_status():
    connected = check_database_connection()

    return {
        "database": "MongoDB Atlas",
        "connected": connected
    }


# Save an email
@app.post("/api/emails")
def create_email(email: EmailCreate):
    try:
        result = save_email(
            email.model_dump()
        )
        return result

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Could not save email"
        )


# Retrieve all emails
@app.get("/api/emails")
def read_emails():
    try:
        emails = get_all_emails()

        return {
            "total": len(emails),
            "emails": emails
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve emails"
        )


# Retrieve one email
@app.get("/api/emails/{gmail_message_id}")
def read_email(gmail_message_id: str):
    email = get_email_by_id(gmail_message_id)

    if not email:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )

    return email
