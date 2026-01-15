import base64
from bs4 import BeautifulSoup


def get_header(headers, name):
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""


def extract_email_data(message):
    payload = message["payload"]
    headers = payload.get("headers", [])

    sender = get_header(headers, "From")
    subject = get_header(headers, "Subject")
    date = get_header(headers, "Date")

    body = ""

    def decode_part(data):
        return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

    if "parts" in payload:
        for part in payload["parts"]:
            mime = part.get("mimeType", "")
            data = part.get("body", {}).get("data")

            if not data:
                continue

            decoded = decode_part(data)

            if mime == "text/plain":
                body = decoded
                break

            elif mime == "text/html" and not body:
                soup = BeautifulSoup(decoded, "html.parser")
                body = soup.get_text(separator=" ", strip=True)

    else:
        data = payload.get("body", {}).get("data")
        if data:
            decoded = decode_part(data)
            soup = BeautifulSoup(decoded, "html.parser")
            body = soup.get_text(separator=" ", strip=True)

    return {
        "from": sender,
        "subject": subject,
        "date": date,
        "content": body
    }
