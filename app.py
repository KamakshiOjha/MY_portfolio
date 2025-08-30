from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os, smtplib, ssl
from email.message import EmailMessage
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET', 'change-me-please')

MAIL_HOST = os.getenv('MAIL_HOST')
MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
MAIL_USER = os.getenv('MAIL_USER')
MAIL_PASS = os.getenv('MAIL_PASS')
MAIL_TO = os.getenv('MAIL_TO', MAIL_USER)

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name','').strip()
    email = request.form.get('email','').strip()
    company = request.form.get('company','').strip()
    message = request.form.get('message','').strip()

    if not name or not email or not message:
        flash('Please fill name, email and message.', 'error')
        return redirect(url_for('index') + '#contact')

    subject = f"Portfolio message from {name}{' @ ' + company if company else ''}"
    body = f"Name: {name}\nEmail: {email}\nCompany: {company}\n\nMessage:\n{message}"

    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = MAIL_USER or email
        msg['To'] = MAIL_TO

        context = ssl.create_default_context()
        with smtplib.SMTP(MAIL_HOST, MAIL_PORT) as server:
            server.ehlo()
            if MAIL_PORT == 587:
                server.starttls(context=context)
            server.login(MAIL_USER, MAIL_PASS)
            server.send_message(msg)
        flash('Thanks! Your message was sent.', 'success')
    except Exception as e:
        print('Email error:', e)
        flash('Could not send message: Email failed to send.', 'error')

    return redirect(url_for('index') + '#contact')

@app.route('/health')
def health():
    return jsonify({'ok': True})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV')!='production')
