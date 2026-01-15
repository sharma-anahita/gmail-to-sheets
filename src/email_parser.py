import base64

def get_header(headers, name):
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""

def extract_email_data(message):
    """
    Extract From, Subject, Date, and plain-text body from Gmail message.
    """

    payload = message["payload"]
    headers = payload.get("headers", [])

    sender = get_header(headers, "From")
    subject = get_header(headers, "Subject")
    date = get_header(headers, "Date")

    body = ""

    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                data = part["body"].get("data")
                if data:
                    body = base64.urlsafe_b64decode(data).decode("utf-8")
                    break
    else:
        data = payload["body"].get("data")
        if data:
            body = base64.urlsafe_b64decode(data).decode("utf-8")

    return {
        "from": sender,
        "subject": subject,
        "date": date,
        "content": body.strip()
    }
