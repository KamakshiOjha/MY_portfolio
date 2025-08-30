# Kamakshi Flask Portfolio

Flask portfolio with a contact form that sends email via SMTP (smtplib).

## Quick start
1. Create and activate virtualenv:
   python -m venv venv
   source venv/bin/activate   # macOS / Linux
   venv\Scripts\activate    # Windows PowerShell
2. pip install -r requirements.txt
3. cp .env.example .env and fill values (use Gmail App Password for MAIL_PASS)
4. python app.py
5. Open http://localhost:5000
