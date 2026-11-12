
from datetime import datetime, timezone
from app.database import emails_collection


# Create a unique index to prevent duplicate Gmail emails
emails_collection.create_index(
    "gmail_message_id",
    unique=True
)


def save_email(email_data):
    """
    Save a new email or update an existing email.
    """

    email_data["updated_at"] = datetime.now(timezone.utc)

    result = emails_collection.update_one(
        {"gmail_message_id": email_data["gmail_message_id"]},
        {"$set": email_data},
        upsert=True
    )

    return {
        "success": True,
        "message": "Email saved successfully",
        "inserted": result.upserted_id is not None
    }


def get_all_emails():
    """
    Retrieve all stored emails.
    """

    emails = list(
        emails_collection.find().sort("received_at", -1)
    )

    for email in emails:
        email["_id"] = str(email["_id"])

    return emails


def get_email_by_id(gmail_message_id):
    """
    Retrieve one email using its Gmail message ID.
    """

    email = emails_collection.find_one(
        {"gmail_message_id": gmail_message_id}
    )

    if email:
        email["_id"] = str(email["_id"])

    return email


def delete_email(gmail_message_id):
    """
    Delete an email record from our application database.
    This does not delete the original Gmail message.
    """

    result = emails_collection.delete_one(
        {"gmail_message_id": gmail_message_id}
    )

    return result.deleted_count > 0
