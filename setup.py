#!/usr/bin/env python

from setuptools import setup, find_packages
import nexentaedge

setup(name='nexentaedge',
      version=nexentaedge.__version__,
      packages=find_packages(),
      description='NexentaEdge configuration package',
      author='Anton Skriptsov',
      author_email='anton.skriptsov@nexenta.com',
     )

