#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()


requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Diana Sargsyan",
    author_email='diana_sargsyan2@edu.aua.am',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A package that implements the Thompson Sampling approach for a Multi-Armed Bandit.",
    license="MIT license",
    include_package_data=True,
    keywords='tsampling',
    name='tsampling',
    packages=find_packages(include=['tsampling', 'tsampling.*']),
    test_suite='tests',
    url='https://github.com/dianasargsyan/tsampling.git',
    version='0.0.1',
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["typing", "numpy", "seaborn", "matplotlib", "pandas"],
    tests_require=["pytest"],
)
