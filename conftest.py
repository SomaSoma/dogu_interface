# -*- coding: utf-8 -*-
import sys
from dogu_interface import init_dogu_interface_test


def default_run_with_cgi(application):

    environ = {}

    # default CGI

    environ['HTTP_METHOD'] = 'POST'
    environ['PROTOCOL_VERSION'] = 'HTTP/2.0'
    environ['SCRIPT_NAME'] = 'test.py'
    environ['PATH_INFO'] = '/test/http'
    environ['QUERY_STRING'] = 'a=b&c=헬로'
    environ['CONTENT_TYPE'] = 'text/plain'
    environ['CONTENT_LENGTH'] = '10'
    environ['SERVER_NAME'] = '10.203.0.1'
    environ['SERVER_PORT'] = '80'

    environ['HTTP_ACCEPT'] = 'text/html; q=0.8, image/jpeg, */* '
    environ['HTTP_USER_AGENT'] = 'Mozila/5.0'

    environ['REMOTE_ADDR'] = '10.10.1.1'

    # wsgi v 1.0.1

    environ['wsgi.input'] = sys.stdin
    environ['wsgi.errors'] = sys.stderr
    environ['wsgi.version'] = (1, 0)
    environ['wsgi.multithread'] = False
    environ['wsgi.multiprocess'] = True
    environ['wsgi.run_once'] = True
    environ['wsgi.url_scheme'] = 'https'

    # callable objects

    def write(data):
        if type(data) is not bytearray and type(data) is not str:
            raise ValueError()

    def start_response(status, response_headers, exc_info=None):
        if type(status) is not str or len(status) == 0:
            raise ValueError()

        if type(response_headers) is not list:
            raise ValueError()
        else:
            for response_header in response_headers:
                if type(response_header) is not tuple:
                    raise ValueError()

        if exc_info is not None and type(exc_info) is not dict:
            raise ValueError()

        return write

    def push_handler(push_headers):
        if type(push_headers) is not list:
            raise ValueError()
        else:
            for response_header in push_headers:
                if type(response_header) is not tuple:
                    raise ValueError()

        # need to call application but it will cause recursive in testing

        return True

    # dogu v 1.0

    environ['dogu.version'] = (1, 0)
    environ['dogu.push'] = push_handler
    environ['dogu.push_enabled'] = True

    result = application(environ, start_response)

    for data in result:
        if data:    # don't send headers until body appears
            write(data)


def pytest_generate_tests(metafunc):

    init_dogu_interface_test(metafunc, {"default": default_run_with_cgi})
