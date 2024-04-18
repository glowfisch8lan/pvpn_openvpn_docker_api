class ValidationException(Exception):
    code = 422
    error_code = 1005
    msg = 'error validate input data'
