#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import io
import setuptools

setuptools.setup(name='combine_signatures',
    version='0.1.0',
    description='Combine signatures of functions.',
    keywords='combine_signatures',
    author='sdpkjc',
    author_email='pazyx728@gmail.com',
    url='https://github.com/sdpkjc/combine-signatures',
    license='GPL-3.0',
    long_description=io.open(
        './README.md', 'r', encoding='utf-8').read(),
    platforms='any',
    classifiers=['Development Status :: 1 - Planning',
                'Programming Language :: Python',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.8',
                'Programming Language :: Python :: 3.8',
                'Programming Language :: Python :: 3.9',
                'Programming Language :: Python :: 3.10',
                'Programming Language :: Python :: 3.11',
                ],
    packages=setuptools.find_packages(),
)
