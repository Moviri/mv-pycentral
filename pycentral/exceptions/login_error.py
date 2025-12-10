# (C) Copyright 2025 Hewlett Packard Enterprise Development LP.
# MIT License

from pycentral.exceptions.pycentral_error import PycentralError


class LoginError(PycentralError):
    """Exception raised when login or authentication fails.

    This exception is raised when authentication to HPE Aruba Networking Central fails,
    typically due to invalid credentials, expired tokens, or network issues.

    Attributes:
        base_msg (str): The base error message for this exception type.
        message (str): Detailed error message describing the login failure.
        status_code (int): HTTP status code associated with the login failure, if available.

    Example:
        ```python
        >>> raise LoginError(msg, status_code)
        LoginError: LOGIN ERROR - Invalid client or client credentials. for
        new_central. Provide valid client_id and client_secret to create an
        access token. (status_code=401)
        ```
    """

    base_msg = "LOGIN ERROR"

    def __init__(self, *args):
        self.message = None
        self.status_code = None
        if args:
            msg = ", ".join((self.base_msg, str(args[0])))
            if len(args) > 1:
                self.status_code = args[1]
                msg = ", ".join(
                    str(a)
                    for a in (
                        msg,
                        *args[1:][1:],
                    )
                )
            self.message = msg
        else:
            self.message = self.base_msg
