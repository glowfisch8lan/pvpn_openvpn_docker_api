from ...base.Controller import Controller
from flask import jsonify


class MainController(Controller):
    """docstring"""

    def __init__(self):
        """Constructor"""
        super().__init__()

    def index(self):
        return jsonify({
            "status": "true",
            "data": 'v1'
        })
