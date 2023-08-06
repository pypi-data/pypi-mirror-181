from bash2py.base import Bash
import json


class Etcd(Bash):
    commands = ['get', 'set', 'delete', 'watch',
                'get_all', 'get_queue', 'set_queue', 'delete_queue', 'watch_queue', 'add_to_queue', 'get_from_queue',
                'delete_from_queue',
                'get_dir', 'set_dir', 'delete_dir', 'watch_dir', 'add_to_dir', 'remove_from_dir',
                ]
    commands_with_value_needed = ['set', 'add_to_queue', 'add_to_dir']

    @staticmethod
    def run(command: commands, key: str = None, value: str = None, host: str = '127.0.0.1',
            port: int = 2379, prefix: str = 'http') -> json:
        """
        Run an etcd command and return the output.
        :param prefix: Your etcd uses {http}s or {https}
        :param value: if there are data to be sent with the request
        :param command:a type of operator (string)
        :param key: the key to be fetched
        :param host: the etcd host
        :param port: the etcd port
        :return: a json object
        """

        if command not in Etcd.commands:
            raise ValueError(f'Invalid command: {command}')

        if command in Etcd.commands_with_value_needed and value is None:
            raise ValueError('Value is needed for this command')

        if prefix not in ['http', 'https']:
            raise ValueError('Invalid prefix')

        if command != 'get_all' and key is None:
            raise ValueError('Key is needed for this command')

        if command == 'get':
            run_command = f'curl -s {prefix}://{host}:{port}/v2/keys/{key}'
        elif command == 'set':
            run_command = f'curl -X PUT {prefix}://{host}:{port}/v2/keys/{key} -d value={value}'
        elif command == 'delete':
            run_command = f'curl -X DELETE {prefix}://{host}:{port}/v2/keys/{key}'
        elif command == 'watch':
            run_command = f'curl -s {prefix}://{host}:{port}/v2/keys/{key}?wait=true'
        elif command == 'get_all':
            run_command = f'curl -s {prefix}://{host}:{port}/v2/keys'
        elif command == 'get_queue':
            run_command = f'curl -s {prefix}://{host}:{port}/v2/keys/queue/{key}'
        elif command == 'set_queue':
            run_command = f'curl -X PUT {prefix}://{host}:{port}/v2/keys/queue/{key}'
        elif command == 'delete_queue':
            run_command = f'curl -X DELETE {prefix}://{host}:{port}/v2/keys/queue/{key}'
        elif command == 'watch_queue':
            run_command = f'curl -s {prefix}://{host}:{port}/v2/keys/queue/{key}?wait=true'
        elif command == 'add_to_queue':
            run_command = f'curl -X PUT {prefix}://{host}:{port}/v2/keys/queue/{key} -d value={value}'
        elif command == 'get_from_queue':
            run_command = f'curl -s {prefix}://{host}:{port}/v2/keys/queue/{key}'
        elif command == 'delete_from_queue':
            run_command = f'curl -X DELETE {prefix}://{host}:{port}/v2/keys/queue/{key}'
        elif command == 'set_dir':
            run_command = f'curl -X PUT {prefix}://{host}:{port}/v2/keys/{key}?dir=true'
        elif command == 'delete_dir':
            run_command = f'curl -X DELETE {prefix}://{host}:{port}/v2/keys/{key}?dir=true'
        elif command == 'get_dir':
            run_command = f'curl -s {prefix}://{host}:{port}/v2/keys/{key}?dir=true'
        elif command == 'watch_dir':
            run_command = f'curl -s {prefix}://{host}:{port}/v2/keys/{key}?dir=true&wait=true'
        elif command == 'add_to_dir':
            run_command = f'curl -X PUT {prefix}://{host}:{port}/v2/keys/{key} -d value={value}'
        elif command == 'remove_from_dir':
            run_command = f'curl -X DELETE {prefix}://{host}:{port}/v2/keys/{key}'
        else:
            raise ValueError(f'Invalid command: {command}')

        run = Bash.do(run_command)
        if run['status']:
            return json.loads(run['logs'])

        raise Exception(run['logs'])

