import time
from googleapiclient.errors import HttpError


def get_sheets_service(creds):
    from googleapiclient.discovery import build
    return build("sheets", "v4", credentials=creds)


def append_row(service, spreadsheet_id, row, retries=3):
    for attempt in range(retries):
        try:
            service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range="Sheet1!A:D",
                valueInputOption="RAW",
                insertDataOption="INSERT_ROWS",
                body={"values": [row]}
            ).execute()
            return

        except HttpError as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise
