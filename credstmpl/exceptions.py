class CredsTmplException(Exception):
    pass

class CredsNotFoundException(CredsTmplException):
    """ This is the exception thrown when we request a nonexistent
        credential.

        It contains an extra field, 'secret', which contains the
        nonexistent secret that was requested.
    """
    def __init__(self, message, secret):
        super(CredsNotFoundException, self).__init__(message)
        self.secret = secret
