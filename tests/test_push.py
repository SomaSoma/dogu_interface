
def test_dogu_features(dogu_handler):
    def application(environ, start_response):
        assert environ.get('dogu.push') is not None
        assert hasattr(environ.get('dogu.push'), '__call__')

        def push_application(environ, start_response):
            return bytearray()

        environ['dogu.push']([('Accept', 'text/html, text/css')], push_application)

        return bytearray()

    dogu_handler(application)
