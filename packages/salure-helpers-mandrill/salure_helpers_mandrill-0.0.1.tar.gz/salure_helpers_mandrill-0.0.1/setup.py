from setuptools import setup


setup(
    name='salure_helpers_mandrill',
    version='0.0.1',
    description='Mandrill wrapper from Salure',
    long_description='Mandrill wrapper from Salure',
    author='D&A Salure',
    author_email='support@salureconnnect.com',
    packages=["salure_helpers.mandrill"],
    license='Salure License',
    install_requires=[
        'salure-helpers-salureconnect>=1',
        'mandrill-really-maintained>=1,<=2'
    ],
    zip_safe=False,
)