from bash2py.curl import Curl
import mock


def test_parse():
    assert Curl.parse('HTTP/2 200 OK\n\n<html>') == {'status_code': 200, 'body': '<html>'}


def test_call():
    with mock.patch('bash2py.base.Bash.do', return_value={'logs': 'HTTP/2 200 OK\n\n<html>', 'status': True}):
        assert Curl.call('http://localhost', 'GET')['status_code'] == 200
        assert Curl.call('https://localhost', 'GET')['status_code'] == 200
