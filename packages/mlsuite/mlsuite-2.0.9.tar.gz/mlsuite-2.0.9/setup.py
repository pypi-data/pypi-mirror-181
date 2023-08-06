#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import find_packages, setup
from glob import glob
from os.path import dirname, join
import os

setup(
    name='mlsuite',
    version='2.0.9',
    description='The traditional machine learning analysis based on sklearn package',
    author='suxing li',
    author_email='li.suxing@genecast.com.cn',
    maintainer='suxing li',
    maintainer_email='li.suxing@genecast.com.cn',
    packages=find_packages(where='.', exclude=(), include=('*',)),
    include_package_data=True,
    platforms=['all'],
    url='https://git.genecast.com.cn/narwhal/mlsuite',
    scripts=['./mlsuite.py'],
    install_requires=[
        'lightgbm >= 2.2.1',
        'joblib >= 0.13.2',
        'numpy >= 1.16.4',
        'pandas >= 0.24.2',
        'scikit-learn >= 0.21.2',
        'sklearn_pandas >= 1.8.0',
        'xgboost >= 1.6.1'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
	"Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Visualization",
    ]
)
