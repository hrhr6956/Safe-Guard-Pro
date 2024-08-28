import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, smtp_username, smtp_password):
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Open the file in binary mode
    with open(attachment_path, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {attachment_path}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to SMTP server and send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Secure the connection
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, text)

# Example usage:
sender_email = "hr66510@outlook.com"
receiver_email = "hr665101@gmail.com"
subject = "Email with Attachment"
body = "This is a test email with an attachment."
attachment_path = "test.jpg"
smtp_server = "smtp-mail.outlook.com"
smtp_port = 587  # For SSL use 465
smtp_username = "hr66510@outlook.com"
smtp_password = "Thatsfunibruh123!"

send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, smtp_username, smtp_password)
