from setuptools import setup


setup(
    name='salure_helpers_sqlserver',
    version='1.0.0',
    description='SQL Server wrapper from Salure',
    long_description='Profit wrapper from Salure',
    author='D&A Salure',
    author_email='support@salureconnnect.com',
    packages=["salure_helpers.sqlserver"],
    license='Salure License',
    install_requires=[
        'salure-helpers-salureconnect>=1',
        'pandas>=1,<=1.35',
        'pymysql>=1,<=2',
        'requests>=2,<=3'
    ],
    zip_safe=False,
)