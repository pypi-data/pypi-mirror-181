#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='OmniSpectrum',
    version = 0.1,
    description=(
        '全向地震动反应谱生成程序'
    ),
    long_description=open('README.md').read(),
    author = 'Guochang Li',
    author_email = 'liguochangli@gmail.com',
    url = 'http://umr.ink',
    license = 'Apache 3.0',
    packages = ['omnispectrum'],
    platforms = ["all"],
    install_requires = [
        'pandas',
        'numpy',
        'matplotlib',
        'scipy',
        'tqdm',
        'python-docx'
    ],
)
