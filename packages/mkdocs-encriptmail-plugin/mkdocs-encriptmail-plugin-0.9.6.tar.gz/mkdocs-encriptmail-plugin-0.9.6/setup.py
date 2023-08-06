# setup.py

import os
from setuptools import setup, find_packages

def read_file(fname):
    "Read a local file"
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='mkdocs-encriptmail-plugin',
    version='0.9.6',
    description='A MkDocs plugin that converts markdown encoded email-links into spambot save <a href> elements.',
	long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    keywords='mkdocs python markdown',
    url='https://github.com/Rolfff/mkdocs-encriptmail-plugin',
    author='Rolfff',
	license='MIT',
	python_requires='>=3.5',
    install_requires=[
		'mkdocs'
	],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'mkdocs.plugins': [
            'encriptmail = src:encriptMailPlugin',
        ]
    }
)