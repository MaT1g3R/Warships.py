import re

from setuptools import find_packages, setup


def get_const(name, text):
    return re.search(
        r'^{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(name), text, re.MULTILINE
    ).group(1)


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md') as f:
    readme = f.read()

with open('wowspy/__init__.py') as f:
    t = f.read()
    version = get_const('__version__', t)
    title = get_const('__title__', t)
    license_ = get_const('__license__', t)
    author = get_const('__author__', t)

setup(
    name=title,
    version=version,
    packages=find_packages(),
    url='https://github.com/MaT1g3R/Warships.py',
    license=license_,
    author=author,
    author_email='mat1g3r@gmail.com',
    description='A Python World of Warships API wrapper',
    install_requires=requirements,
    long_description=readme,
    include_package_data=True,
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
