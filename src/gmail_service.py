import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes define what the app can do
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/spreadsheets"
]


def get_gmail_service():
    """
    Authenticates the user and returns a Gmail API service instance.
    Uses OAuth 2.0 and stores token for reuse.
    """

    creds = None
    token_path = "credentials/token.pickle"
    creds_path = "credentials/credentials.json"

    # Load existing token if available
    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    # If no valid credentials, start OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for next run
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    # Build Gmail service
    service = build("gmail", "v1", credentials=creds)
    return service, creds


def fetch_unread_emails(service, max_results=10):
    """
    Fetch unread emails from the inbox.
    Returns a list of full message objects.
    """

    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"],
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])

    full_messages = []
    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()
        full_messages.append(msg_data)

    return full_messages

def mark_as_read(service, message_id):
    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={"removeLabelIds": ["UNREAD"]}
    ).execute()
