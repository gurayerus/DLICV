#!/usr/bin/env python3
"""Setup tool for DLICV."""
__author__ 	= 'Guray Erus'

import setuptools
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()

if sys.version_info >= (3, 9, 0):
	sys.exit('Python versions 3.9 and higher are not supported.')

if sys.version_info < (3, 6):
	sys.exit('Python version prior to 3.6 are not supported.')

setuptools.setup(
    name="DLICV",
    version="0.1.0",
    author="Guray Erus",
    author_email="software@cbica.upenn.edu",
	python_requires=">=3.6",
    description="Deep Learning based ICV Segmentation on T1 MRI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gurayerus/DLICV",
    packages=setuptools.find_packages(),
	install_requires=[
	'scipy==1.5.4',
	'matplotlib==3.3.3',
	'tensorflow==2.3.3',
	'tensorflow-addons==0.13.0',
	'dill==0.3.4',
	'h5py==2.10.0',
	'hyperopt==0.2.5',
	'keras==2.6.0',
	'numpy==1.18.5',
	'protobuf==3.17.3',
	'pymongo==3.12.0',
	'scikit-learn==0.24.2',
	'nibabel==3.2.1',
	'resource==0.2.1',
	'networkx==2.5.1'
	],
	entry_points = {
    'console_scripts': ['dlicv_downloadmodel=DLICV.dlicv_downloadmodel:_main', 'dlicv_apply=DLICV.dlicv_apply:_main'],
    },
    classifiers=(
		"Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ),
)

