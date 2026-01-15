# Gmail to Google Sheets Automation

**Author:** Anahita Sharma

---

## 📖 Project Overview

This project is a Python-based automation system that reads unread emails from a Gmail inbox and logs them into a Google Sheet. Each qualifying email is processed exactly once and appended as a new row in the sheet.

The system uses:
- **Gmail API** to read and manage emails
- **Google Sheets API** to store structured email data
- **OAuth 2.0 authentication** for secure access

---

## 🎯 Objective

For every unread email in the inbox, the script logs the following fields into Google Sheets:

| Column | Description |
|--------|-------------|
| From | Sender email address |
| Subject | Email subject line |
| Date | Date and time the email was received |
| Content | Email body (plain text) |

---

## 🏗️ High-Level Architecture

```
Gmail Inbox (Unread Emails)
         ↓
   Gmail API (OAuth 2.0)
         ↓
  Python Application
    ├── Email Parsing
    ├── HTML → Text Conversion
    ├── Duplicate Prevention
    └── Logging & Retry Logic
         ↓
  Google Sheets API
         ↓
Google Sheet (Append Rows)
```

---

## 📂 Project Structure

```
gmail-to-sheets/
│
├── src/
│   ├── gmail_service.py      # Gmail OAuth & email operations
│   ├── sheets_service.py     # Google Sheets append logic
│   ├── email_parser.py       # Header + body parsing (HTML → text)
│   ├── logger.py             # Centralized logging configuration
│   └── main.py               # End-to-end pipeline
│
├── credentials/
│   └── credentials.json      # OAuth client credentials (NOT committed)
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/sharma-anahita/gmail-to-sheets
cd gmail-to-sheets
```

### 2️⃣ Create & Activate Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Google Cloud Configuration

1. Create a [Google Cloud Project](https://console.cloud.google.com/)
2. Enable **Gmail API** and **Google Sheets API**
3. Configure OAuth consent screen (External for personal use)
4. Create **Desktop App OAuth 2.0 credentials**
5. Download `credentials.json` and place it in: `credentials/credentials.json`

### 5️⃣ Run the Script

```bash
python src/main.py
```

**On first run:**
- Browser opens for OAuth consent
- After granting access, a token is generated
- Token is automatically reused on subsequent runs

---

## 🔐 Authentication Approach

This project uses the **OAuth 2.0 Installed App flow**:

1. Application identifies itself using `client_id` from `credentials.json`
2. User explicitly grants Gmail and Sheets access via browser consent
3. Google issues a scoped access token
4. Token is stored locally and reused without repeated consent

This approach ensures:
- No password storage
- User-controlled access
- Compliance with Google security best practices

---

## 🔁 Duplicate Prevention Strategy

**Method:** Label-based state management

- Only emails with the `UNREAD` label are fetched from Gmail
- After successful processing, emails are marked as `READ`
- Re-running the script automatically skips already processed emails

**Benefits:**
- No duplicate rows in Google Sheets
- No external database required
- Simple, reliable, and scalable approach

---

## ✉️ Email Parsing Logic

**Header Extraction:**
- `From`, `Subject`, and `Date` fields are extracted from Gmail API metadata

**Body Extraction:**
- Prioritizes `text/plain` content when available
- If only `text/html` exists, converts to plain text using **BeautifulSoup**
- Ensures clean, readable content in Google Sheets

---

## 📊 Logging Implementation

The project uses Python's `logging` module for:
- Timestamped execution logs
- Real-time processing visibility
- Easier debugging and monitoring

**Example output:**
```
2026-01-15 11:46:43 - INFO - Starting Gmail to Sheets automation
2026-01-15 11:46:43 - INFO - Processing 5 unread emails
2026-01-15 11:46:45 - INFO - Processed email: Invoice January
2026-01-15 11:46:46 - INFO - Run completed successfully
```

---

## 🔄 Retry Logic for Reliability

Google Sheets API calls include **exponential backoff retry logic**:
- Automatically retries transient network or quota failures
- Configurable retry attempts and delays
- Prevents partial data loss during temporary issues

---

## 🧪 Proof of Execution

The `/proof` folder contains:

1. **Screenshots:**
   - Unread emails in Gmail inbox
   - Google Sheet populated with email data
   - OAuth consent screen

2. **Video walkthrough (2-3 minutes):**
   - Project architecture explanation
   - Gmail → Sheets data flow demonstration
   - Duplicate prevention mechanism
   - Script re-run behavior

---

## 🚧 Challenges & Solutions

### Challenge 1: OAuth Access Blocked for Unverified App
**Solution:** Configured test users in Google Cloud Console and used the "Advanced → Allow" option during OAuth consent, which is appropriate for personal/internal automation tools.

### Challenge 2: Raw HTML Appearing in Sheets
**Solution:** Implemented HTML-to-plain-text conversion using BeautifulSoup's `get_text()` method to extract clean, readable content.

### Challenge 3: Duplicate Email Processing
**Solution:** Used Gmail's label system (`UNREAD` → `READ`) as a natural state indicator, eliminating the need for external tracking.

---

## ⚠️ Known Limitations

- Processes only unread emails from the inbox (excludes spam, trash, other folders)
- Does not handle email attachments
- Designed for personal or small-scale usage (not optimized for high-volume ingestion)
- Limited to 100 emails per API call (pagination implemented if needed)

---

## ⭐ Bonus Features

- **HTML-to-plain-text conversion** for readable email bodies
- **Structured logging** with timestamps for debugging
- **Retry logic** with exponential backoff for API resilience
- **Modular code structure** for easy maintenance and extension

---

## 📦 Dependencies

Key libraries used:
- `google-auth` - OAuth 2.0 authentication
- `google-api-python-client` - Gmail and Sheets API clients
- `beautifulsoup4` - HTML parsing
- `python-dateutil` - Date parsing

Full list available in `requirements.txt`

---

## 🔒 Security Considerations

- `credentials.json` and `token.json` are excluded via `.gitignore`
- OAuth tokens stored locally with appropriate file permissions
- API scopes limited to minimum required permissions
- No sensitive data hardcoded in source files

---

 

## ✅ Conclusion

This project demonstrates:
- **Secure API integration** using OAuth 2.0
- **Clean software architecture** with separation of concerns
- **Production-ready practices** including logging and error handling
- **Reliable automation** with built-in duplicate prevention

The solution is simple, maintainable, and follows industry best practices for Python automation projects.
 
