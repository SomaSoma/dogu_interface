# -*- coding: utf-8 -*-


def init_dogu_interface_test(metafunc, dogu_handlers):

    if 'dogu_handler' in metafunc.fixturenames:
        argvalues = []
        ids = []

        for dogu_handler in dogu_handlers.items():
            ids.append(dogu_handler[0])
            argvalues.append(dogu_handler[1])

        metafunc.parametrize(argnames='dogu_handler', argvalues=argvalues, ids=ids, scope='function')
