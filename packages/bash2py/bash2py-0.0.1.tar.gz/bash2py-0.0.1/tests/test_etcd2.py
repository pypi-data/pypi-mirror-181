from bash2py.etcd2 import Etcd
import mock
import json


def test_get():
    with mock.patch('bash2py.base.Bash.do',
                    return_value={'logs': json.dumps({"node": {"value": "value"}}), 'status': True}):
        assert Etcd.run('get', 'key')['node']['value'] == 'value'


def test_set():
    with mock.patch('bash2py.base.Bash.do',
                    return_value={'logs': json.dumps({"node": {"value": "value"}}), 'status': True}):
        assert Etcd.run('set', 'key', 'value')['node']['value'] == 'value'


def test_delete():
    with mock.patch('bash2py.base.Bash.do',
                    return_value={'logs': json.dumps(
                        {"action": "delete", "node": {"key": "/key", "modifiedIndex": 9, "createdIndex": 8},
                         "prevNode": {"key": "/key", "value": "value", "modifiedIndex": 8, "createdIndex": 8}}),
                        'status': True}):
        assert Etcd.run('delete', 'key') is not None


def test_watch():
    with mock.patch('bash2py.base.Bash.do',
                    return_value={'logs': json.dumps({"node": {"value": "value"}}), 'status': True}):
        assert Etcd.run('watch', 'key') is not None


def test_get_all():
    with mock.patch('bash2py.base.Bash.do',
                    return_value={'logs': json.dumps({"node": {"value": "value"}}), 'status': True}):
        assert Etcd.run('get_all') is not None
