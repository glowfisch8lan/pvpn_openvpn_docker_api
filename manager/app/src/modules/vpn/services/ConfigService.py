import random
import string
from src.base.BaseService import BaseService
import os

from src.modules.vpn.services.CertService import CertService

host = os.getenv('DOMAIN_CONTROLLER')
username = os.getenv('DOMAIN_ACCOUNT')
password = os.getenv('DOMAIN_PASSWORD')


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class ConfigService(BaseService):

    def __init__(self):
        self.certService = CertService()
        super().__init__()

    def create(self, ca_cert_file_path, ca_key_file_path, ta_key_file_path, dh_key_file_path, cn, common_path,
               duration):
        login = cn
        cn = cn + '_' + randomword(10)
        # Read our common options file first
        f = open(common_path, 'r')
        common = f.read()
        f.close()

        cacert = self.certService.retrieve_cert(ca_cert_file_path)
        cakey = self.certService.retrieve_key(ca_key_file_path)

        with open(ta_key_file_path, 'r') as file:
            takey = file.read()

        with open(ta_key_file_path, 'r') as file:
            takey = file.read()

        key = self.certService.make_keypair()
        csr = self.certService.make_csr(key, cn)
        # with open(os.getenv("PKI_CSR_KEY_PATH") + output_ovpn + '.req', 'w') as file:
        #     file.write(self.certService.dump_file_in_mem(csr).decode("utf-8"))
        crt = self.certService.create_slave_certificate(csr, cakey, cacert, 0x0C, duration)

        clientkey = self.certService.dump_file_in_mem(key)
        # with open(os.getenv("PKI_PRIVATE_KEY_PATH") + output_ovpn + '.key', 'w') as file:
        #     file.write(clientkey.decode("utf-8"))

        clientcert = self.certService.dump_file_in_mem(crt)
        # with open(os.getenv("PKI_CERT_KEY_PATH") + output_ovpn + '.crt', 'w') as file:
        #     file.write(clientcert.decode("utf-8"))

        cacertdump = self.certService.dump_file_in_mem(cacert)
        # tacertdump = self.certService.dump_file_in_mem(takey)
        # dhkeydump = self.certService.dump_file_in_mem(dhkey)

        ovpn = "%s\n" \
               "<ca>\n%s\n</ca>" \
               "\n<cert>\n%s</cert>\n" \
               "<key>\n%s</key>\n" \
               "\n<tls-auth>\n%s\n</tls-auth>\n" \
               "%s" % (
            common,
            cacertdump.decode(),
            clientcert.decode(),
            clientkey.decode(),
            takey,
            'remote' + os.getenv('HOST_ADDR') + ' ' + os.getenv('VPN_PORT')
        )

        # Write our file.
        f = open('vpn/' + cn + '.ovpn', 'w')
        f.write(ovpn)
        f.close()

        return cn
