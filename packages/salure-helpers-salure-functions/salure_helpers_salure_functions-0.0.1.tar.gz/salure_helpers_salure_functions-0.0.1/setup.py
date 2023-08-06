from setuptools import setup


setup(
    name='salure_helpers_salure_functions',
    version='0.0.1',
    description='Helpful functions from Salure',
    long_description='Helpful functions from Salure',
    author='D&A Salure',
    author_email='support@salureconnnect.com',
    packages=["salure_helpers.salure_functions"],
    license='Salure License',
    install_requires=[
        'salure-helpers-salureconnect>=1',
        'salure-helpers-mysql>=0',
        'pandas>=1,<=1.35',
        'requests>=2,<=3'
    ],
    zip_safe=False,
)