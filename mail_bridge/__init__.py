from .main import send_email
from .exceptions import (
    ConfigurationError,
    AuthenticationError,
    RecipientsRefusedError,
    SenderRefusedError,
    SMTPGenericError,
    EmailEncodingError
)
