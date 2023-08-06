from setuptools import setup


setup(
    name='salure_helpers_mysql',
    version='0.0.1',
    description='MySQL wrapper from Salure',
    long_description='MySQL wrapper from Salure',
    author='D&A Salure',
    author_email='support@salureconnnect.com',
    packages=["salure_helpers.mysql"],
    license='Salure License',
    install_requires=[
        'salure-helpers-salureconnect>=1',
        'pandas>=1,<=1.35',
        'pymysql>=1,<=2',
        'requests>=2,<=3'
    ],
    zip_safe=False,
)