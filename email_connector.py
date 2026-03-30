# import smtplib
# from email.mime.text import MIMEText

# sender_email = "vishnuvardhan1691@gmail.com"
# app_password = "buyn zbxi vpnw uvpl"

# receiver_email = "bhavan@aerele.in"  # test with your own email

# msg = MIMEText("Hello! This is a test email from Python.")
# msg["Subject"] = "Test Email"
# msg["From"] = sender_email
# msg["To"] = receiver_email

# try:
#     with smtplib.SMTP("smtp.gmail.com", 587) as server:
#         server.starttls()
#         server.login(sender_email, app_password)
#         server.sendmail(sender_email, receiver_email, msg.as_string())

#     print("✅ Email sent successfully")

# except Exception as e:
#     print("❌ Error:", e)