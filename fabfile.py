from fabric.api import *
import lithium

def tag():
    local('git tag -sm "lithium {0}" {0}'.format(lithium.__version__))
    local('git push origin {}'.format(lithium.__version__))

def upload():
    local('python setup.py sdist register upload')

def release():
    tag()
    upload()
