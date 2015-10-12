import subprocess

from . exceptions import CredsNotFoundException, LastPassNotFoundException

def lookup(secret, field):
    """ This looks up the secret using Last Pass CLI.

        :param secret:  The secret to look for. Will raise a
                        CredsNotFound exception if not found.
                        Will raise LastPassNotFound exception if
                        Last Pass CLI is not installed.
        :param field:   The field to extract.
    """
    try:
        return subprocess.check_output(["lpass", "show", "--field={}".format(field), secret], stderr=subprocess.STDOUT)
    except OSError as e:
        raise LastPassNotFoundException(e)
    except subprocess.CalledProcessError as e:
        raise CredsNotFoundException(e.output, secret)
