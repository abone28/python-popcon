#!/usr/bin/env python

from distutils.core import setup

setup(name='python-popcon',
        version='1.1',
        description="Python inteface to Debian's popcon database",
        author='Bastian Venthur',
        author_email='venthur@debian.org',
        url='http://github.com/venthur/python-popcon',
        packages=['popcon'],
        package_dir={"": "src"},
        scripts=["scripts/popcon_snap2db", "scripts/popcon_stat2db"],
        )

