# -*- coding: utf-8 -*-
from setuptools import setup
import sys
sys.path.append('./src')
sys.path.append('./test')
version = file('VERSION').read().strip()

setup(name='shopicruit_2016',
      version=version,
      description="Solution to the Shopify intern 2016 problem",
      long_description=file('README').read(),
      classifiers=[],
      keywords=('python optimization purchase'),
      author='Carlos Campana',
      author_email='campanacue@gmail.com',
      url='https://github.com/cccue/shopicruit_2016',
      license='MIT License',
      package_dir={'': 'src'},
      packages=['shopicruit_2016'],
      install_requires=["numpy","jsonschema","urllib3"],
      test_suite = 'test_shopicruit_2016.suite'
      )

