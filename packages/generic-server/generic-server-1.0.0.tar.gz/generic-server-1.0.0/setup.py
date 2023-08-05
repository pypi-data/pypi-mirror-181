from setuptools import setup, find_packages

setup(name='generic-server',
      version='1.0.0',
      packages=find_packages(),
      entry_points = {
          'console_scripts': ['genericserver=genericserver.__main__:main'],
          }
     )
