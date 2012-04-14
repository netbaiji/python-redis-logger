try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='python-redis-logger',
    version='0.1.3',
    description='Persistent redis logger for python',
    author='Teodor Pripoae',
    author_email='toni@netbaiji.com',
    url='https://github.com/teodor-pripoae/python-redis-logger',
    install_requires=['redis'],
    packages=['redis_logger'])
