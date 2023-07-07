from src.base.BaseService import BaseService
from OpenSSL import crypto


class CertService(BaseService):

    def __init__(self):
        super().__init__()

    def make_keypair(self, algorithm=crypto.TYPE_RSA, numbits=2048):
        pkey = crypto.PKey()
        pkey.generate_key(algorithm, numbits)
        return pkey

    # Creates a certificate signing request (CSR) given the specified subject attributes.
    def make_csr(self, pkey, CN, C=None, ST=None, L=None, O=None, OU=None, emailAddress=None,
                 hashalgorithm='sha256WithRSAEncryption'):
        req = crypto.X509Req()
        req.get_subject()
        subj = req.get_subject()

        if C:
            subj.C = C
        if ST:
            subj.ST = ST
        if L:
            subj.L = L
        if O:
            subj.O = O
        if OU:
            subj.OU = OU
        if CN:
            subj.CN = CN
        if emailAddress:
            subj.emailAddress = emailAddress

        req.set_pubkey(pkey)
        req.sign(pkey, hashalgorithm)
        return req

    # Create a certificate authority (if we need one)
    def create_ca(self, CN, C="", ST="", L="", O="", OU="", emailAddress="", hashalgorithm='sha256WithRSAEncryption'):
        cakey = self.make_keypair()
        careq = self.make_csr(cakey, cn=CN)
        cacert = crypto.X509()
        cacert.set_serial_number(0)
        cacert.gmtime_adj_notBefore(0)
        cacert.gmtime_adj_notAfter(60 * 60 * 24 * 365 * 10)  # 10 yrs - hard to beat this kind of cert!
        cacert.set_issuer(careq.get_subject())
        cacert.set_subject(careq.get_subject())
        cacert.set_pubkey(careq.get_pubkey())
        cacert.set_version(2)

        # Set the extensions in two passes
        cacert.add_extensions([
            crypto.X509Extension('basicConstraints', True, 'CA:TRUE'),
            crypto.X509Extension('subjectKeyIdentifier', True, 'hash', subject=cacert)
        ])

        # ... now we can set the authority key since it depends on the subject key
        cacert.add_extensions([
            crypto.X509Extension('authorityKeyIdentifier', False, 'issuer:always, keyid:always', issuer=cacert,
                                 subject=cacert)
        ])

        cacert.sign(cakey, hashalgorithm)
        return cacert, cakey

    # Create a new slave cert.
    def create_slave_certificate(self, csr, cakey, cacert, serial, duration):
        cert = crypto.X509()
        cert.set_serial_number(serial)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(duration)  # Полдня
        cert.set_issuer(cacert.get_subject())
        cert.set_subject(csr.get_subject())
        cert.set_pubkey(csr.get_pubkey())
        cert.set_version(2)

        extensions = [crypto.X509Extension(b'basicConstraints', False, b'CA:FALSE'),
                      crypto.X509Extension(b'subjectKeyIdentifier', False, b'hash', subject=cert),
                      crypto.X509Extension(b'authorityKeyIdentifier', False, b'keyid:always,issuer:always',
                                           subject=cacert,
                                           issuer=cacert),
                      crypto.X509Extension(b'extendedKeyUsage', False, b'clientAuth'),
                      crypto.X509Extension(b"keyUsage", False, b"digitalSignature")]
        cert.add_extensions(extensions)
        cert.sign(cakey, 'sha256WithRSAEncryption')

        return cert

    # Dumps content to a string
    def dump_file_in_mem(self, material, format=crypto.FILETYPE_PEM):
        dump_func = None
        if isinstance(material, crypto.X509):
            dump_func = crypto.dump_certificate
        elif isinstance(material, crypto.PKey):
            dump_func = crypto.dump_privatekey
        elif isinstance(material, crypto.X509Req):
            dump_func = crypto.dump_certificate_request
        else:
            raise Exception("Don't know how to dump content type to file: %s (%r)" % (type(material), material))

        return dump_func(format, material)

    def load_from_buffer(self, file, objtype, format=crypto.FILETYPE_PEM):
        if objtype is crypto.X509:
            load_func = crypto.load_certificate
        elif objtype is crypto.X509Req:
            load_func = crypto.load_certificate_request
        elif objtype is crypto.PKey:
            load_func = crypto.load_privatekey
        else:
            raise Exception("Unsupported material type: %s" % (objtype,))

        buf = file

        material = load_func(format, buf)
        return material

    # Loads the file into the appropriate openssl object type.
    def load_from_file(self, materialfile, objtype, format=crypto.FILETYPE_PEM):
        if objtype is crypto.X509:
            load_func = crypto.load_certificate
        elif objtype is crypto.X509Req:
            load_func = crypto.load_certificate_request
        elif objtype is crypto.PKey:
            load_func = crypto.load_privatekey
        else:
            raise Exception("Unsupported material type: %s" % (objtype,))

        with open(materialfile, 'r') as fp:
            buf = fp.read()

        material = load_func(format, buf)
        return material

    def retrieve_key(self, ca_key_file_path, passphrase=None):
        # load CA key
        with open(ca_key_file_path, "r") as f:
            ca_key_buf = bytes(f.read(), 'utf-8')
            ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, ca_key_buf, passphrase)
            return ca_key

    def retrieve_cert(self, ca_cert_file_path):
        # load CA cert
        with open(ca_cert_file_path, "r") as f:
            ca_cert_buf = bytes(f.read(), 'utf-8')
            ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, ca_cert_buf)
            return ca_cert

    def retrieve_key_from_file(self, keyfile, passphrase):
        return self.load_from_file(keyfile, crypto.PKey, passphrase)

    def retrieve_csr_from_file(self, csrfile):
        return self.load_from_file(csrfile, crypto.X509Req)

    def retrieve_cert_from_file(self, certfile):
        return self.load_from_file(certfile, crypto.X509)
