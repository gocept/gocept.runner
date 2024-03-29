from setuptools import find_packages
from setuptools import setup
import os.path


def read(*names):
    return open(os.path.join(os.path.dirname(__file__), *names)).read()


setup(
    name='gocept.runner',
    version='3.1.dev0',
    description="Create stand alone programs with full Zope3 runtime"
                " environment",
    long_description="\n\n".join([
        read('README.rst'),
        read('src', 'gocept', 'runner', 'appmain.rst'),
        read('src', 'gocept', 'runner', 'once.rst'),
        read('src', 'gocept', 'runner', 'README.rst'),
        read('src', 'gocept', 'runner', 'transaction.rst'),
        read('CHANGES.rst'),
    ]),
    classifiers=[
        "Topic :: Software Development",
        "Framework :: Zope :: 3",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "License :: OSI Approved :: Zope Public License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="zope3 mainloop",
    author="gocept gmbh & co. kg",
    author_email="mail@gocept.com",
    url='https://github.com/gocept/gocept.runner',
    license="ZPL 2.1",
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    namespace_packages=['gocept'],
    python_requires='>=3.7',
    install_requires=[
        'ZODB',
        'decorator',
        'setuptools',
        'transaction',
        'zope.app.appsetup>=3.6.0',
        'zope.app.wsgi',
        'zope.authentication',
        'zope.component',
        'zope.publisher',
        'zope.security',
        'zope.testing',
    ],
    extras_require=dict(
        test=[
            'gocept.testing>=1.1',
            'mock',
            'zope.app.appsetup>=3.6.0',
            'zope.app.testing',
            'zope.app.zcmlfiles',
            'zope.securitypolicy',
        ],
    ),
    entry_points=dict(
        console_scripts=[
            'runexample = gocept.runner.example:example',
        ],
    ),
)
