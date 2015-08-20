
def test_start_response(dogu_handler):
    def application(environ, start_response):
        if environ['dogu.push']:
            pass

        return bytearray()

    dogu_handler(application)
