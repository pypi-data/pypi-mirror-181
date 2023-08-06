import enum

from bash2py.base import Bash
import re


class Curl(Bash):
    methods: str = {'GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'}

    @staticmethod
    def parse(logs: str) -> dict:
        """
        Parse the output of the curl command and return a dict with the status code and the body
        the command will look like this: curl -w "\n---%{http_code}---" http://example.com
        the output will look like this: <html>...---200---
        :param logs: the output of the curl command
        :return: a dict containing the status code and the body
        """
        status_code_regex = re.compile(r'HTTP\/[0-9a-zA-Z.]* ([0-9]{3})')
        body_regex = re.compile(r'\n\n(.*)')
        status_code = status_code_regex.search(logs).group(1)
        if status_code:
            body = body_regex.search(logs).group(1)
            return {'status_code': int(status_code), 'body': body}
        return {'status_code': 0, 'body': logs}

    @staticmethod
    def call(url: str, method: methods, data: str = None, with_output: str = None, self_cert: bool = False, auth: tuple = None) -> dict:
        """
        Run a curl command and return the output and status code.
        :param data: if there are data to be sent with the request
        :param with_output: to download the body of the response
        :param self_cert: when you want to use a self-signed certificate
        :param auth: if auth is provided, the command will look like this: curl -u user
        :param method: one of the items from the methods set
        :param url: the url to be fetched
        :return: a dict containing the output and the status code
        """
        if method not in Curl.methods:
            raise ValueError(f'Invalid method: {method}')
        addition = ""
        if auth:
            addition = '-u {auth[0]}:{auth[1]}'.format(auth=auth)
        if self_cert:
            addition += ' --insecure -k'
        if with_output:
            addition += f' -o {with_output}'
        if data:
            addition += f' -d {data}'
        command = f'curl -s -L {addition} -i -X {method} {url}'
        run = Bash.do(command)
        if run['status']:
            response = Curl.parse(run['logs'])  # parse the output
            return response

        raise Exception(run['logs'])

