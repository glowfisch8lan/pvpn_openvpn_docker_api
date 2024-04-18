import os
from http.client import HTTPException

from flask import request

from src.base.exceptions.ForbiddenException import ForbiddenException


class AuthMiddleware:
    """docstring"""

    def __init__(self):
        """Constructor"""

    def handle(self) -> None:
        # if request.headers.get('AUTH') != os.getenv("AUTH_KEY"):
        #     raise ForbiddenException
        return None
