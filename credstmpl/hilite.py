def ok(text):
    # ansi escape sequences for colors, this one uses GREEN
    return '\033[92m{}\033[0m'.format(text)

def bad(text):
    # ansi escape sequences for colors, this one uses RED
    return '\033[91m{}\033[0m'.format(text)
