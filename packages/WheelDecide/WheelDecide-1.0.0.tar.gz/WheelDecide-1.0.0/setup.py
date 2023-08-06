#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

with open('README.rst','r',encoding="utf8") as f:
    long_description=f.read()

setup(
    name='WheelDecide',
    version='1.0.0',
    description=(
        'This is a package which can make a wheel to decide.'
    ),
    long_description=long_description,
    author='Jason4zh',
    author_email='13640817984@163.com',
    maintainer='Jason4zh',
    maintainer_email='13640817984@163.com',
    license='BSD License',
    packages=find_packages(),
    platforms=['all'],
    url='https://github.com/Jason4zh/WheelDecide',
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
