import base64
import os
import re
from datetime import datetime

from OpenSSL import crypto
from werkzeug.utils import secure_filename

from .services.CertService import CertService
from .services.ConfigService import ConfigService
from ...base.Controller import Controller
from flask import jsonify, request, send_file

ALLOWED_EXTENSIONS = {'vpn'}


class ConfigController(Controller):
    """docstring"""

    def __init__(self):
        """Constructor"""
        super().__init__()

    def create(self):
        ca_cert_file_path = '/app/keys/ca.crt'
        ca_key_file_path = '/app/keys/ca.key'
        ta_key_file_path = '/app/keys/ta.key'
        dh_key_file_path = '/app/keys/dh.pem'
        common_path = '/app/common/common.ovpn'

        if request.is_json:
            data = request.get_json()
        else:
            return ''

        if not 'duration' in data:
            raise ValueError('No duration time for key expire')

        if not 'cn' in data:
            raise ValueError('No cn name')

        filename = ConfigService().create(
            ca_cert_file_path,
            ca_key_file_path,
            ta_key_file_path,
            dh_key_file_path,
            data['cn'],
            common_path,
            data['duration']
        )
        content = open(r'/app/vpn/' + filename + '.ovpn')
        encoded = base64.b64encode(content.read().encode())
        return {'name': filename, 'file': encoded.decode('utf-8')}

    def info(self):
        file = request.files.get('file')
        filename = secure_filename(file.filename)
        config = file.stream.read()

        certService = CertService()
        ca = re.search(r'<ca>(.+?)</ca>', str(config))
        ca = ca[1].replace(r'\n', '\n')
        ca = certService.load_from_buffer(ca, crypto.X509)

        cert = re.search(r'<cert>(.+?)</cert>', str(config))
        cert = cert[1].replace(r'\n', '\n')
        cert = certService.load_from_buffer(cert, crypto.X509)
        cnObject = cert.get_subject()

        return jsonify({
            'ca': {
                'not_after': datetime.strptime(ca.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ'),
                'not_before': datetime.strptime(ca.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ'),
            },
            'cert': {
                'not_after': datetime.strptime(cert.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ'),
                'not_before': datetime.strptime(cert.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ'),
            },
            'cn': cnObject.CN
        })

    def download_file(self, cn):
        filename = cn
        requested_path = '/app/vpn/' + cn.replace('.ovpn', '') + '.ovpn'
        return send_file(os.fspath(requested_path), mimetype='application/vpn', download_name=filename + '.ovpn',
                         as_attachment=True)
