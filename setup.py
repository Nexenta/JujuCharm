#!/usr/bin/env python

from setuptools import setup, find_packages
import nexentaedge_configurator

setup(name='nexentaedge_configurator',
      version=nexentaedge_configurator.__version__,
      packages=find_packages(),
      description='NexentaEdge configuration package',
      author='Anton Skriptsov',
      author_email='anton.skriptsov@nexenta.com',
     )

