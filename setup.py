#!/usr/bin/env python
from setuptools import setup, find_packages


def install():

    setup(
        name='dogu_interface',
        version='1.2',
        description='WSGI extension Inteface for HTTP/2',
        long_description='WSGI extension Inteface for HTTP/2',
        author='Luavis Kang',
        author_email='luaviskang@gmail.com',
        url='https://github.com/SomaSoma/dogu_interface',
        classifiers=[
            'Development Status :: 1 - Planning',
            'License :: Freeware',
            'Operating System :: POSIX',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: MacOS :: MacOS X',
            'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4'],
        packages=find_packages(),
        install_requires=[
            'pytest==2.7.2',
        ],
    )

if __name__ == "__main__":
    install()
