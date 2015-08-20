import inspect

def test_write(dogu_handler):
    def application(environ, start_response):

        write = start_response('200 OK', [()])
        assert hasattr(write, '__call__')
        assert inspect.getargspec(write)[0] == ['data']

        write(bytearray(10))

        return bytearray()

    dogu_handler(application)


def test_invalid_write(dogu_handler):
    def application(environ, start_response):

        try:
            write = start_response('200 OK', [()])
            write(0)  # write int is invalid
        except ValueError:
            assert True
        else:
            assert False  # status is not str but it doesn't make error

        return bytearray()

    dogu_handler(application)
