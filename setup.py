from setuptools import setup, find_packages

setup(
    name='dhp_ingestion_tool_common',
    version='0.1.0',
    description='Library for DHP ingestion tool',
    author='Lam Tran',
    author_email='lamtt26@fpt.com',
    packages=find_packages(exclude=['*tests*']),
)