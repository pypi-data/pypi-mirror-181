from bash2py.base import Bash


class OpenSSL(Bash):
    @staticmethod
    def create_ca_files(HOST: str, ROOT: str, LOCATION: str, AGE: int = 36500,
                        OPENSSL_CNF: str = '/usr/lib/ssl/openssl.cnf'):
        """
        Create files for a local CA
        :param HOST:
        :param ROOT:
        :param OPENSSL_CNF:
        :param LOCATION:
        :param AGE:
        :return:
        """
        Bash.do(f'mkdir -p {LOCATION}', False)
        first_step = Bash.do(
            f'openssl req -new -nodes -text -out {LOCATION}/{ROOT}.pem -keyout {LOCATION}/{ROOT}.key -subj /CN={ROOT}.{HOST}')
        second_step = Bash.do(
            f'openssl x509 -req -in {LOCATION}/{ROOT}.pem -text -days {AGE} -extfile {OPENSSL_CNF} -extensions v3_ca -signkey {LOCATION}/{ROOT}.key -out {LOCATION}/{ROOT}.crt')
        assert first_step['status'] and second_step[
            'status'], f'Failed to create CA files: {first_step["logs"]} {second_step["logs"]}'
        # Set authorizations
        Bash.do(f'chmod 400 {LOCATION}/{ROOT}.key')
        Bash.do(f'chmod 444 {LOCATION}/{ROOT}.crt')
        Bash.do(f'chmod 444 {LOCATION}/{ROOT}.pem')
        return True

    @staticmethod
    def create_server_files(FILENAME: str, SUBJ: str, root: str, LOCATION: str, ROOT_LOCATION: str, AGE: int = 36500):
        """
        Create files for a local server
        :param FILENAME:
        :param ROOT_LOCATION:
        :param root:
        :param LOCATION:
        :param SUBJ:
        :param AGE:
        :return:
        """
        key = LOCATION + '/' + FILENAME + '.key'
        req = LOCATION + '/' + FILENAME + '.req'
        crt = LOCATION + '/' + FILENAME + '.crt'
        root = ROOT_LOCATION + '/' + root
        first_step = Bash.do(f'openssl genrsa -out {key} 2048')
        second_step = Bash.do(f'openssl req -new -sha256 -key {key} -out {req} -subj {SUBJ}')
        third_step = Bash.do(f'openssl x509 -req -in {req} -text -days {AGE} -CA {root}.crt -CAkey {root}.key -CAcreateserial -out {crt}')
        assert first_step['status'] and second_step['status'] and third_step['status'], f'Failed to create server files: {first_step["logs"]} {second_step["logs"]} {third_step["logs"]}'
        # Set authorizations
        Bash.do(f'chmod 400 {key}')
        Bash.do(f'chmod 444 {crt}')
        Bash.do(f'chmod 444 {req}')
        return True
