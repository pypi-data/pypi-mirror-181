#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='MovingClock',
    version='1.0.0',
    description=(
        'This is a package which can make a MovingClock'
    ),
    long_description=open('README.rst').read(),
    author='Jason4zh',
    author_email='13640817984@163.com',
    maintainer='Jason4zh',
    maintainer_email='13640817984@163.com',
    license='BSD License',
    packages=find_packages(),
    platforms=['all'],
    url='https://github.com/Jason4zh/MovingClock',
    install_requires=[
        "zhdate",
        "os",
        "random",
        "turtle",
        "datetime"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ]
)
