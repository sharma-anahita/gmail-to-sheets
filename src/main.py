from gmail_service import get_gmail_service, fetch_unread_emails, mark_as_read
from email_parser import extract_email_data
from sheets_service import get_sheets_service, append_row

SPREADSHEET_ID = "1phj35bFlqZ4eJlBZYAa0eFyPXHJzU1ideXpXDvqIu3o"

def main():
    gmail_service, creds = get_gmail_service()
    sheets_service = get_sheets_service(creds)

    messages = fetch_unread_emails(gmail_service)

    print(f"Processing {len(messages)} unread emails")

    for msg in messages:
        data = extract_email_data(msg)

        row = [
            data["from"],
            data["subject"],
            data["date"],
            data["content"]
        ]

        append_row(sheets_service, SPREADSHEET_ID, row)
        mark_as_read(gmail_service, msg["id"])

    print("Done!")

if __name__ == "__main__":
    main()
