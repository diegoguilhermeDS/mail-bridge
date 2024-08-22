import dotenv
import os
import smtplib
from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

from .exceptions import (
    AuthenticationError,
    EmailEncodingError,
    SMTPGenericError,
    SenderRefusedError,
    RecipientsRefusedError,
    MailBridgeError,
    ConfigurationError
)

# Load environment variables from .env file
dotenv.load_dotenv()

# Access environment variables
SENDER = os.getenv("SENDER")
PASSWORD = os.getenv("PASSWORD_EMAIL_SENDER")
RECIPIENT = os.getenv("RECIPIENT")
SMTP_SERVER = "smtp.office365.com"
PORT = 587

if not all([SENDER, PASSWORD, RECIPIENT]):
    raise ConfigurationError("SENDER, PASSWORD, and RECIPIENT must all be provided.")


def create_email_message(sender, recipient, subject, body, attachment_path):
    """Creates an email message with the specified parameters."""
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject

    # Attach body
    msg.attach(MIMEText(body, "html"))

    # Attach file
    if attachment_path:
        attach_file_to_email(msg, attachment_path)

    return msg


def attach_file_to_email(msg, file_path):
    """Attaches a file to the email message."""
    part = MIMEBase("application", "octet-stream")
    with open(file_path, 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)

    today = datetime.today().strftime("%d-%m-%Y")
    time = datetime.now().strftime('%H-%M-%S')
    part.add_header(
        "Content-Disposition",
        f'attachment; filename="santander-producao-{today}_{time}.xlsx"',
    )
    msg.attach(part)


def send_email_via_smtp(msg, password):
    """Sends an email via SMTP with the given message and password."""
    try:
        server = smtplib.SMTP(SMTP_SERVER, PORT)
        server.starttls()
        server.login(msg["From"], password)
        server.sendmail(msg["From"], msg["To"], msg.as_string().encode("utf-8"))
    except smtplib.SMTPAuthenticationError:
        raise AuthenticationError()

    except smtplib.SMTPRecipientsRefused:
        raise RecipientsRefusedError()

    except smtplib.SMTPSenderRefused:
        raise SenderRefusedError()

    except smtplib.SMTPException as e:
        raise SMTPGenericError(f"SMTP error occurred: {str(e)}")

    except UnicodeEncodeError as e:
        raise EmailEncodingError(f"Error encoding email message: {str(e)}")

    except Exception as e:
        raise MailBridgeError(f"An unexpected error occurred: {str(e)}")

    finally:
        server.quit()


def send_email_with_attachment(subject, message, attachment_path=None):
    """Main function to send an email with the Excel file attachment."""
    body = f"""
    <html>
    <body>
        <p>{message}</p>
    </body>
    </html>
    """
    msg = create_email_message(SENDER, RECIPIENT, subject, body, attachment_path)
    send_email_via_smtp(msg, PASSWORD)


def send_email_without_attachment(subject, message, attachment_path=None):
    """Main function to send an email without file attachment."""
    body = f"""
    <html>
    <body>
        <p>Prezados,</p>
        <p>{message}</p>
    </body>
    </html>
    """
    msg = create_email_message(SENDER, RECIPIENT, subject, body, attachment_path)
    send_email_via_smtp(msg, PASSWORD)
