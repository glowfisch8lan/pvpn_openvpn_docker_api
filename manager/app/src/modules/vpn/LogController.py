import os
import tailer
from flask import jsonify
from ...base.Controller import Controller


class LogController(Controller):
    """docstring"""

    def __init__(self):
        """Constructor"""
        super().__init__()

    def log(self):
        openvpn_file_log = os.getenv("OPENVPN_FILE_LOG")

        f = open(openvpn_file_log, 'r')
        log_list = tailer.tail(f, 100)
        f.close()

        return jsonify(log_list)
