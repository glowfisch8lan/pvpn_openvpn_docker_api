import os
import glob
from ...base.Controller import Controller
from flask import jsonify, request
import re


class UserController(Controller):
    """docstring"""

    def __init__(self):
        """Constructor"""
        super().__init__()

    def enable(self):
        if request.is_json:
            data = request.get_json()

            filename = data['cn'].replace('..', '')
            file = './ccd/' + filename
            with open(file, 'r+') as f:
                str = f.read().replace("disable", '')
                new_str = '\n'.join(el.strip() for el in str.split('\n') if el.strip())
                with open(file, 'w') as f:
                    f.write(new_str)

        else:
            return ''
        return jsonify({
            "status": "true",
            "message": "enabled"
        })

    def disable(self):
        if request.is_json:
            data = request.get_json()
            filename = data['cn'].replace('..', '')

            file = './ccd/' + filename

            with open(file, 'w+') as f:
                str = f.read().replace("disable", '')
                new_str = '\n'.join(el.strip() for el in str.split('\n') if el.strip())
                if len(new_str) > 0:
                    new_str += "\ndisable"
                else:
                    new_str += "disable"

                with open(file, 'w') as f:
                    f.write(new_str)

        else:
            return ''
        return jsonify({
            "status": "true",
            "message": "disabled"
        })

    def connected(self):
        openvpn_file_status = os.getenv("OPENVPN_FILE_STATUS")
        # if request.headers.get('AUTH') != os.getenv("CA_CERT_FILE_PATH"):
        #     return app.response_class(
        #         response='',
        #         status=403,
        #         mimetype='application/json'
        #     )

        keys = []
        list_array = []

        f = open(openvpn_file_status, "r")
        line_index = 0
        while True:
            line_index += 1
            # считываем строку
            line = f.readline()
            # прерываем цикл, если строка пустая
            if line_index == 3:
                keys = line.split(",")

            if line_index > 3 & line.find('ROUTING TABLE') != False:
                values = line.split(',')
                list_array.append(dict(zip(keys, values)))

            if not line or line.find('ROUTING TABLE') == 0:
                break

        f.close()

        return jsonify(list_array)

    def routing(self):
        openvpn_file_status = os.getenv("OPENVPN_FILE_STATUS")

        keys = []
        parse = False
        listRoutes = []
        # dictA = dict(zip(list1, list2))
        f = open(openvpn_file_status, "r")
        line_index = 0
        while True:
            line_index += 1
            # считываем строку
            line = f.readline()

            if line.find('GLOBAL STATS') == 0:
                break

            if parse:
                values = line.split(',')
                listRoutes.append(dict(zip(keys, values)))

            if line.find('ROUTING TABLE') == 0:
                keys = next(f).split(",")
                parse = True

        f.close()

        return jsonify(listRoutes)

    def keys(self):
        login = request.args.get('login')
        search_dir = "vpn/"
        files = list(filter(os.path.isfile, glob.glob(
            search_dir + login + '_??????????.ovpn')))  # WARNING ЕСЛИ БУДЕМ ГЕНЕРИРОВАТЬ больше 10-ти символов, иметь то ввиду
        files.sort(key=lambda x: os.path.getmtime(x))
        lastKey = files[-1] if len(files) > 0 else ""
        s = lastKey
        match = re.search(r'vpn\/(.*)\.ovpn', s)
        if match is None:
            fileName = None
        else:
            fileName = match[1]

        return jsonify({
            "status": "true",
            "data": fileName
        })
