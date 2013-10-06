__version__ = '1.0'
__copyright__ = 'Copyright (c) 2011-2013, Kyle Fuller'
__licence__ = 'BSD'
__author__ = 'Kyle Fuller <inbox@kylefuller.co.uk>'
__URL__ = 'http://github.com/kylef/lithium/'

def templates_path():
    from os.path import dirname, join
    return join(dirname(__file__), 'templates')

