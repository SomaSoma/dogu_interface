import inspect


def test_push_handler_callable(dogu_handler):
    def application(environ, start_response):
        assert environ.get('dogu.push') is not None
        assert hasattr(environ.get('dogu.push'), '__call__')

        assert(
            inspect.getargspec(environ.get('dogu.push'))[0] == ['push_headers']
        )

        def push_application(environ, start_response):
            return bytearray()

        environ['dogu.push'](
            [('Accept', 'text/html, text/css')]
        )

        start_response('200 OK', [])

        return bytearray()

    dogu_handler(application)


def test_push_enabled_valid(dogu_handler):
    def application(environ, start_response):

        assert environ['dogu.push_enabled']

        if environ['PROTOCOL_VERSION'] <= 'HTTP/1.1':
            assert environ['dogu.push_enabled'] is False

        start_response('200 OK', [])
        return bytearray()

    dogu_handler(application)
