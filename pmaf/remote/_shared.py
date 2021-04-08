from email.utils import parseaddr


def validate_email(email_str):
    ret = False
    parsed_email = parseaddr(email_str)
    if parsed_email != ('',''):
        ret = True
    return ret

