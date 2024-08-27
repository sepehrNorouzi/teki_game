import secrets
import string
import time


def generate_unique_string(prefix: str, length=8, all_digit=False):
    timestamp = str(int(time.time()))
    characters = string.digits
    if not all_digit:
        characters += string.ascii_letters
    unique_string = ''.join(secrets.choice(characters) for _ in range(length - len(timestamp)))
    return f"{prefix}-{unique_string}{timestamp[-len(timestamp):]}"
