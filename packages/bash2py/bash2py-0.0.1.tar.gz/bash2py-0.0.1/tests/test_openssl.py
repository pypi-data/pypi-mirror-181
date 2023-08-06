from bash2py.base import Bash
from bash2py.openssl import OpenSSL


def test_create_ca_files():
    Bash.do('rm -rf /tmp/ca_test')
    assert OpenSSL.create_ca_files('localhost', 'root', '/tmp/ca_test')


def test_create_server_files():
    assert OpenSSL.create_server_files('server', '/CN=server.localhost', 'root', '/tmp/ca_test', '/tmp/ca_test')
