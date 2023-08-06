from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description  =  fh.read()

setup(
    name = 'phyengine',
    version = '1.5.0.0',
    description = 'Pyhton library for simple physics modelation',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/tacterex/PhyEngine',
    author = 'tacterex',
    license = 'MIT',
    packages = ['phyengine'],
    install_requires = ['keyboard', 'openpyxl'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
    ]
)