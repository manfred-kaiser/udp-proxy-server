# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='udp_proxy_server',
    version='0.0.2',
    author='Manfred Kaiser',
    author_email='manfred.kaiser@logfile.at',
    description='udp proxy server to intercept udp',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    url="https://github.com/manfred-kaiser/udp-proxy-server",
    python_requires='>= 3.5',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: System :: Networking"
    ],
    entry_points={
        'console_scripts': [
            "udp2tcp = udp_proxy_server.cli:udp2tcp"
        ]
    },
    install_requires=[
        'enhancements'
    ]
)
