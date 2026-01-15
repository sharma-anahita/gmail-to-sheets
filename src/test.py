from gmail_service import get_gmail_service, fetch_unread_emails, mark_as_read
from email_parser import extract_email_data

service = get_gmail_service()

messages = fetch_unread_emails(service)

print(f"Found {len(messages)} unread emails\n")

for msg in messages:
    data = extract_email_data(msg)
    print("FROM:", data["from"])
    print("SUBJECT:", data["subject"])
    print("DATE:", data["date"])
    print("CONTENT:", data["content"][:200])
    print("-" * 40)

    mark_as_read(service, msg["id"])
