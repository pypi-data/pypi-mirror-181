import bash2py.base
from bash2py.base import Bash
from config import Config


def test_do():
    assert 'success' in Bash.do('echo success')['logs']
    assert '[Errno 2]' in Bash.do('run_random_program')['logs'] and Bash.do('run_random_program')['status'] is False
    assert Bash.do(9999, False)['status'] is False


def test_run_script():
    Bash.rm('/tmp/read.echo.sh')
    Bash.rm('/tmp/input.txt')
    Bash.rm('/tmp/output.txt')
    with open(Config.BASE_DIR + '/tests/utils/read.echo.run') as f:
        s = f.read()
        f = open('/tmp/read.echo.sh', "w")
        f.write(s)
        f.close()
        Bash.chmod('/tmp/read.echo.sh', '750')

    with open(Config.BASE_DIR + '/tests/utils/input.txt') as f:
        s = f.read()
        f = open('/tmp/input.txt', "w")
        f.write(s)
        f.close()
        Bash.chmod('/tmp/input.txt', '750')

    assert Bash.run_script('/tmp/read.echo.sh', ['/tmp/input.txt', '/tmp/output.txt'])['status'] is True



