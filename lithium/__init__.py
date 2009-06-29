__version__ = 0.2
__copyright__ = 'Copyright (c) 2008, Kyle Fuller'
__licence__ = 'BSD'
__author__ = 'Kyle Fuller <inbox@kylefuller.co.uk>'
__URL__ = 'http://kylefuller.co.uk/project/lithium/'

def templates_path():
    from os.path import dirname, join
    return join(dirname(__file__), 'templates')
