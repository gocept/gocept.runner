from setuptools import setup, find_packages

setup(name='gocept.runner',
      version='0.1dev',
      description="",
      long_description="""\
""",
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[],
      keywords="",
      author="",
      author_email="",
      url="",
      license="",
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'zope.app.twisted',
          'zope.app.wsgi',
          'zope.testing',
      ],
      extras_require=dict(
          test=['zope.securitypolicy',
                'zope.app.testing']),
      entry_points = dict(
        console_scripts =
          ['runexample = gocept.runner.example:example'])
     )
