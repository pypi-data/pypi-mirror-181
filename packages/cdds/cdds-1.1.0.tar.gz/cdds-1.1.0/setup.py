#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# pre dojo-env updating to python 3.9
# requirements = ['Click>=7.0', 'numpy>=1.21.6, <=1.22.4','missingno==0.5.1', 'pandas>=1.3.5, <=1.4.2', 
# 'seaborn>=0.11.0', 'matplotlib>=3.2.2, <=3.4.3', 'scikit-learn>=0.23.1, <=1.1.*', 
# 'scipy==1.8.*','IPython','ipywidgets==8.0.2','tzlocal','pyperclip']
requirements = ['Click>=7.0', 'numpy','missingno', 'pandas>=1.3.5', 'seaborn>=0.11.0', 
'matplotlib>=3.2.2', 'scikit-learn>=1.1.3', 'scipy','IPython','ipywidgets','tzlocal','pyperclip']

test_requirements = [*requirements ]

setup(
    author="James Irving",
    author_email='james.irving.phd@gmail.com',
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
    description="Package for coding dojo data science students and staff.",
    entry_points={
        'console_scripts': [
            'cdds=cdds.cli:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='cdds',
    name='cdds',
    packages=find_packages(include=['cdds', 'cdds.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jirvingphd/cdds',
    version='1.1.0',
    zip_safe=False,
)
