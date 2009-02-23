lithium is a set of applications written for the Django web framework. lithium is a disposable battery which can be used on any Django website.

lithium currently includes:

- [Blog](/projects/lithium/blog/) - A simple web-logging application which can be used for multi-user, multi-domain websites.
- [Contact](/projects/lithium/contact/) - Contact allow users of your website to easily sent you a email over a web-based form.

Applications which are not quite finished:

- Media - A application which allows a user to store audio, photos, and videos. This will allow photo galleries, and will hopefully allow attaching photos to blog posts, as well as audio for podcasting.
- Store - A small e-commence system with support for PayPal and Google Checkout.
- Wiki - A wiki application which allows users to contribute and edit pages.
- Forum - A powerful forum application which allows permission based forums.
- Groups - Allowing a group based profile, where the group can have a set of pages, and there own blog.
- Profiles - A user profile module allowing users to become friends of one and another.

### Dependencies
I am trying to make lithium not require anything other than standard Python, and Django 1.0. Currently lithium requires a patch to django.contrib.comments which should hopeful be applied to the Django svn. This patch can be found [here](http://code.djangoproject.com/ticket/10285).

Lithium requirements:

- django.contrib.comments
- django.contrib.markup
- [markdown](http://www.freewisdom.org/projects/python-markdown/Installation)

### Downloading lithium
lithium can be downloaded via [zip](http://github.com/kylef/lithium/zipball/master), [tar.gz](http://github.com/kylef/lithium/tarball/master) or the [git repository](http://github.com/kylef/lithium/). It can also be installed via package management systems such as ``easy_install`` and ``pip``.

### Installation
#### Using a package-management tool
The easiest way by far to install lithium and most other Python software is by using an automated package-management tool, if you're not already familiar with the available package management tools Python. Now's is a good time to get started.

One option is [easy_install](http://peak.telecommunity.com/DevCenter/EasyInstall), you can refer to its documentation to see how to get it set up. Once you've got it, you'll be able to type:

    easy_install lithium

Another more popular option is [pip](http://pypi.python.org/pypi/pip/). Once again, refer to its documentation to get pip up and running, but once you have pip all setup and installed, you'll be able to type:

    pip install lithium

#### From source code
If you have git installed on your computer, you can obtain the latest source code by typing:

    git clone git://github.com/kylef/lithium.git

Inside the resulting "lithium" directory will be another directory called "lithium", which is the Python module for lithium; you can symlink this from your Python path, or if you prefer use setup.py (more on that in Manually installing). You could also directly copy lithium to your Python path, but this is not recommended. Symbolic links is one of the best ways for easy upgrading, at a later date, all you need to do is run ``git pull`` from inside lithium folder.

#### Manually installing
To manually install lithium, you will first need to download lithium. Once you have a copy of lithium, open it and run:

    python setup.py install

This will instal lithium and will require administrative privileges on your computer as it is a system-wide install.

Now that you have installed lithium, you can add any lithium sub-module to your Django project. Please see the sub application documentation page for instructions.