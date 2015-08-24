from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='charm.base',
      version=version,
      description="A base for charming",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Whit Morriss',
      author_email='ecosystem-engineering@lists.launchpad.net',
      url='http://juju.solutions/charm.base',
      license='MPL2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            "path.py"
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
