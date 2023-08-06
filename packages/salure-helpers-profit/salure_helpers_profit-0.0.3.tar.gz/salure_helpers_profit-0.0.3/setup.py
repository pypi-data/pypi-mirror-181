from setuptools import setup, find_namespace_packages


setup(
    name='salure_helpers_profit',
    version='0.0.3',
    description='Profit wrapper from Salure',
    long_description='Profit wrapper from Salure',
    author='D&A Salure',
    author_email='support@salureconnnect.com',
    packages=find_namespace_packages(where='salure_helpers_profit'),
    license='Salure License',
    install_requires=[
        'salure-helpers-salureconnect>=0,<=1'
    ],
    zip_safe=False,
)