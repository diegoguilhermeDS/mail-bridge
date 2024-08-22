# exceptions.py
class ConfigurationError(Exception):
    """Exception raised when required configuration variables are not set."""

    def __init__(self, message="Missing required configuration values."):
        super().__init__(message)


class MailBridgeError(Exception):
    """Base exception for errors in the MailBridge library."""
    pass


class AuthenticationError(MailBridgeError):
    """Error raised when authentication with the SMTP server fails."""

    def __init__(self, message=None):
        super().__init__(message or "Failed to authenticate with the SMTP server.")


class RecipientsRefusedError(MailBridgeError):
    """Error raised when all recipients are refused by the SMTP server."""

    def __init__(self, message=None):
        super().__init__(message or "All recipients were refused by the SMTP server.")


class SenderRefusedError(MailBridgeError):
    """Error raised when the sender address is refused by the SMTP server."""

    def __init__(self, message=None):
        super().__init__(message or "The sender address was refused by the SMTP server.")


class SMTPGenericError(MailBridgeError):
    """Generic error raised when an SMTP exception occurs."""

    def __init__(self, message=None):
        super().__init__(message or "An SMTP error occurred.")


class EmailEncodingError(MailBridgeError):
    """Error raised when encoding the email message fails."""

    def __init__(self, message=None):
        super().__init__(message or "Error encoding the email message.")
