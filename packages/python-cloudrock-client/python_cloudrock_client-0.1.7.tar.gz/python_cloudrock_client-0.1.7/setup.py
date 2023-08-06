#!/usr/bin/env python

from setuptools import setup

install_requires = [
    "requests>=2.6.0",
]

tests_requires = [
    "responses>=0.5.0",
    "pytest>=6.2.5",
]

setup(
    name="python-cloudrock-client",
    version="0.1.0",
    author="Cloudrock Team",
    author_email="support@cloudrock.ca",
    url="https://cloudrock.ca",
    license="MIT",
    description="REST client for the Cloudrock API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    tests_require=tests_requires,
    package_dir={"": "src"},
    py_modules=["cloudrock_client"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
