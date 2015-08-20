import re


def test_cgi_features(dogu_handler):

    def application(environ, start_response):
        ###########################
        #   Test CGI variable
        ###########################

        assert environ.get('CONTENT_LENGTH')
        assert type(environ['CONTENT_LENGTH']) is str
        assert environ['CONTENT_LENGTH'].isdigit()

        # test HTTP_METHOD
        assert environ.get('HTTP_METHOD')
        assert type(environ['HTTP_METHOD']) is str
        assert environ['HTTP_METHOD'] in ['HEAD', 'POST', 'GET', 'PUT', 'DELETE']

        # test PROTOCOL_VERSION
        assert environ.get('PROTOCOL_VERSION')
        assert type(environ['PROTOCOL_VERSION']) is str
        assert re.match('^HTTP\/\d\.d$', environ['PROTOCOL_VERSION'])

        # test SCRIPT_NAME
        assert environ.get('SCRIPT_NAME')
        assert type(environ['SCRIPT_NAME']) is str

        # test QUERY_STRING
        assert environ.get('QUERY_STRING')
        assert type(environ['QUERY_STRING']) is str

        # test CONTENT_TYPE
        assert environ.get('CONTENT_TYPE')
        assert type(environ['CONTENT_TYPE']) is str
        assert re.match('\w\/\w', environ['CONTENT_TYPE'])

        # test SERVER_PORT
        assert environ.get('SERVER_PORT')
        assert type(environ['SERVER_PORT']) is str
        assert environ['SERVER_PORT'].isdigit()

        # test HTTP_ACCEPT
        assert environ.get('HTTP_ACCEPT')
        assert type(environ['HTTP_ACCEPT']) is str

        # test HTTP_USER_AGENT
        assert environ.get('HTTP_USER_AGENT')
        assert type(environ['HTTP_USER_AGENT']) is str

        # test REMOTE_ADDR
        assert environ.get('REMOTE_ADDR')
        assert type(environ['REMOTE_ADDR']) is str
        assert re.match('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', environ['REMOTE_ADDR'])

        for x in environ['REMOTE_ADDR'].split('.'):
            assert int(x)

    dogu_handler(application)


def test_wsgi_features(dogu_handler):
    def application(environ, start_response):

        ###########################
        #   Test WSGI variable
        ###########################

        assert environ.get('wsgi.input')
        assert hasattr(environ.get('wsgi.input'), 'read')
        assert hasattr(environ.get('wsgi.input').read, '__call__')

        assert hasattr(environ.get('wsgi.input'), 'readline')
        assert hasattr(environ.get('wsgi.input').readline, '__call__')

        assert environ.get('wsgi.version')
        assert type(environ.get('wsgi.version')) is tuple
        assert len(environ.get('wsgi.version')) == 2

        assert environ.get('wsgi.version')[0] == 1
        assert environ.get('wsgi.version')[1] == 0

        assert environ.get('wsgi.multithread')
        assert type(environ.get('wsgi.multithread')) is bool

        assert environ.get('wsgi.multiprocess')
        assert type(environ.get('wsgi.multiprocess')) is bool

    dogu_handler(application)


def test_dogu_features(dogu_handler):
    def application(environ, start_response):
        ###########################
        #   Test Dogu variable
        ###########################

        assert environ.get('dogu.version')
        assert type(environ.get('dogu.version')) is tuple
        assert len(environ.get('dogu.version')) == 2

        assert environ.get('dogu.version')[0] == 1
        assert environ.get('dogu.version')[1] == 0

        assert environ.get('dogu.push')
        assert hasattr(environ.get('dogu.push'), '__call__')

        assert environ.get('dogu.push_enabled')
        assert type(environ.get('dogu.push_enabled')) is bool

        return bytearray()

    dogu_handler(application)
