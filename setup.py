from setuptools import find_packages, setup

from wowspy import *

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md') as f:
    readme = f.read()

setup(
    name=__title__,
    version=__version__,
    packages=find_packages(),
    url='https://github.com/MaT1g3R/Warships.py',
    license=__license__,
    author=__author__,
    author_email='mat1g3r@gmail.com',
    description='A Python World of Warships API wrapper',
    install_requires=requirements,
    long_description=readme,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ]
)
