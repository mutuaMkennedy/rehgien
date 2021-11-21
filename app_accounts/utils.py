import re

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
phone_regex = r'^\+?1?\d{9,14}$'

def is_email(q):
    return re.fullmatch(email_regex, q)

def is_phone(q):
    return re.fullmatch(phone_regex,q)
