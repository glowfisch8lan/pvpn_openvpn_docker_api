class ForbiddenException(Exception):
    code = 403
    error_code = 1004
    msg = 'forbidden'
