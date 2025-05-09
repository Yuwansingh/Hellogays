from flask import Flask, render_template, request
import os
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    email = request.form['email']
    otp = str(random.randint(100000, 999999))

    msg = MIMEMultipart()
    msg['From'] = f"Free-fire-craftaland<{os.getenv('EMAIL_USER')}>"
    msg['To'] = email
    msg['Subject'] = "Freefirecraftland- OTP Verification Code"

    html = f"""
    <html>
    <body>
      <p>Hello,<br><br>
         Your OTP for login is: <strong>{otp}</strong><br><br>
         Do not share this code. It will expire in 5 minutes.<br><br>
         Regards,<br>
         YourApp Team<br>
         support@yourapp.com
      </p>
    </body>
    </html>
    """
    msg.attach(MIMEText(html, 'html'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
        server.send_message(msg)
        server.quit()
        return "OTP sent successfully!"
    except Exception as e:
        return f"Failed to send OTP: {e}"

if __name__ == '__main__':
    app.run()
