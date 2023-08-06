#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Ani Guloyan",
    author_email='ani.guloyan.13@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python Package for Bass Model",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='bass_model_package',
    name='bass_model_package',
    packages=find_packages(include=['bass_model_package', 'bass_model_package.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ani0813/bass_model_package',
    version='0.1.0',
    zip_safe=False,
)
