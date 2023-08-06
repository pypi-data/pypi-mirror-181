#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: mage
# Created Time:  2022-12-15 22:17:34
#############################################

from distutils.core import Extension
from setuptools import setup, find_packages
# module1 = Extension('gpu_lib',
#                 sources= ['gpu_lib.so'])
setup(
    name = "phe_cuda",
    version = "0.1.3",
    keywords = ("pip", "cuda","phe", "paillier", "mage"),
    description = "Acceleration Paillier by cuda",
    long_description = "Acceleration for Partially Homomorphic Encryption library by Cuda ",
    license = "MIT Licence",

    url = "https://github.com/gxx777/phe_cuda",
    author = "Xiangxin Guo",
    author_email = "xiangxinguo@mail.ustc.edu.cn",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [],
    data_files = [('phe_cuda',['phe_cuda/gpu_lib.so'])]
)
