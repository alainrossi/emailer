import os
from setuptools import setup, find_packages

setup(
    name="emailer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # No external dependencies beyond Python standard library
    ],
    author="Alain ROSSI",
    author_email="aea_rossi@hotmail.com",
    description="A Python package for sending automated emails",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    keywords="email, automation, smtp",
    url="https://github.com/aea_rossi/emailer",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)