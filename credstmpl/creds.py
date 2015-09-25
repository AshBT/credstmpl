import os
from credstash import getSecret, ItemNotFound

from . exceptions import CredsNotFoundException

# get the default AWS region
region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
def lookup(secret):
    """ This closure looks up the secret using credstash. While it is
        possible to cache results so that multiple requests for the
        same secret don't hit AWS multiple times, it's probably safer
        not to store the plaintext secrets in memory.

        :param string:  The secret to look for. Will raise a
                        CredsNotFound exception if not found.
    """
    try:
        return getSecret(secret, region=region)
    except ItemNotFound as e:
        raise CredsNotFoundException(str(e), secret)
