from setuptools import setup

setup(
    name='satori_ingestion',
    version='0.1',
    description='A module to write streaming data from Satori into a simple sqlite db',
    author='Christian Hagel',
    author_email='hagel.christian@googlemail.com',
    packages=['satori_ingestion', 'satori_ingestion.helper'],
    install_requires=['satori-rtm-sdk', 'sqlalchemy', 'pyyaml'],
)
