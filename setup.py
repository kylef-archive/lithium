#!/usr/bin/env python
from distutils.core import setup
import lithium

packages = ['lithium',]
core = ['conf', 'views',]
apps = ['blog', 'contact', 'forum', 'wiki']
templatetags = ['blog',]
package_data = {}
uses_migrations = ['wiki']

for item in templatetags:
    packages.append('lithium.%s.templatetags' % item)

for item in apps + core + templatetags:
    packages.append('lithium.%s' % item)
    if item in uses_migrations:
        packages.append('lithium.%s.migrations' % item)

for app in apps:
    package_data['lithium.%s' % app] = ['templates/%s/*.html' % app, 'templates/%s/*.txt' % app]

setup(
    name='lithium',
    version='%s' % lithium.__version__,
    description="A set of applications for writing a Django website's, it includes a blog, a forum, and many other useful applications.",
    author='Kyle Fuller',
    author_email='inbox@kylefuller.co.uk',
    url='http://github.com/kylef/lithium/',
    download_url='http://github.com/kylef/lithium/zipball/%s' % lithium.__version__,
    packages=packages,
    package_data=package_data,
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
