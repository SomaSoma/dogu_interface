
def test_start_response(dogu_handler):
    def application(environ, start_response):

        start_response('200 OK', [])
        return bytearray()

    dogu_handler(application)
