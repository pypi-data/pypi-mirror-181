# Release process setup see:
# https://github.com/pypa/twine
#
# Upgrade twine
#     python3 -m pip install --user --upgrade twine
#
# Run this to build the `dist/PACKAGE_NAME-xxx.tar.gz` file
#     rm -rf ./dist && python3 setup.py sdist
#
# Check dist/*
#     python3 -m twine check dist/*
#
# Run this to build & upload it to `pypi`, type your account name when prompted.
#     python3 -m twine upload dist/*
#
# In one command line:
#     rm -rf ./dist && python3 setup.py sdist bdist_wheel && python3 -m twine check dist/*
#     rm -rf ./dist && python3 setup.py sdist bdist_wheel && python3 -m twine upload dist/*
#

from setuptools import setup, find_packages

# Usage: python setup.py sdist bdist_wheel

links = []  # for repo urls (dependency_links)

DESCRIPTION = "Django based app for Microsoft authentication of users."
VERSION = "0.1.6"

setup(
    name="django-microsoft-auth-sync",
    version=VERSION,
    author="Shubham Dipt | Ulisses1478",
    author_email="shubham.dipt@gmail.com",
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    url="https://github.com/ulisses1478/django-microsoft-authentication",
    license="MIT",
    packages=['microsoft_authentication', 'microsoft_authentication.auth', 'microsoft_authentication.migrations'],
    platforms=["any"],
    keywords=["django", "microsoft", "authentication"],
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires='msal >= 1.9.0',
    dependency_links=links,
)