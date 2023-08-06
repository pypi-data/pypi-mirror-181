from setuptools import setup


setup(
    name='salure_helpers_profit',
    version='0.0.5',
    description='Profit wrapper from Salure',
    long_description='Profit wrapper from Salure',
    author='D&A Salure',
    author_email='support@salureconnnect.com',
    packages=["salure_helpers.profit"],
    license='Salure License',
    install_requires=[
        'salure-helpers-salureconnect>=0,<=1'
    ],
    zip_safe=False,
)