from setuptools import setup, find_packages

setup(
    name=' pymagic',  
    version='0.1',
    packages=find_packages(),
    install_requires=['pygame'],
    description="A library for creating magic effects in games.",
    long_description=open('README.md').read(),
    author='Houda Izem',
    author_email='houdaizem166@gmail.com',
)
