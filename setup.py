#!/usr/bin/env python3
from setuptools import setup, find_packages

install_requires = [
    "flask-restx==0.5.0",
    "packaging==17.1",
    "pip==9.0.1",
    "requests==2.19.0",
    "setuptools==40.0.0",
    "virtualenv==16.0.0",
    "pyyaml==5.4.1",
    "schematics==2.1.0",
    "PyJWT==1.7.1",
    "ipython",
    "passlib",
    "python-status",
    "jsonschema",
    "stomp.py",
]

tests_require = [
    'httpretty',
]

setup(
    name='teacher_directory',
    version="0.1.0",
    description='a build teacher directory',
    # long_description=open('README.rst').read(),
    author='Directory Services',
    author_email='deepikahirrao@gmail.com',
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Software Distribution',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'teacher_directory=teacher_directory.run:main',
        ],
    },
    tests_require=tests_require
)
