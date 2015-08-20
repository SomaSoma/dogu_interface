import inspect


def test_start_response(dogu_handler):
    def application(environ, start_response):

        assert(
            inspect.getargspec(start_response)[0] == ['status', 'response_headers', 'exc_info']
        )

        assert inspect.getargspec(start_response).defaults == (None,)

        start_response('200 OK', [()])
        return bytearray()

    dogu_handler(application)


def test_invalid_status_start_response(dogu_handler):
    def application(environ, start_response):

        try:
            start_response('', [()])
        except ValueError:
            assert True
        else:
            assert False  # status is empty but it doesn't make error

        try:
            start_response(200, [()])
        except ValueError:
            assert True
        else:
            assert False  # status is not str but it doesn't make error

        start_response('200 OK', [()])

        return bytearray()

    dogu_handler(application)


def test_invalid_response_headers_start_response(dogu_handler):
    def application(environ, start_response):

        try:
            start_response('200 OK', None)
        except ValueError:
            assert True
        else:
            assert False  # headers are invalid but it doesn't make error

        start_response('200 OK', [()])

        return bytearray()

    dogu_handler(application)
