# create setup.py for package

import setuptools

setuptools.setup(
    name="monthinfo",
    version="1.0.1",
    author="Marco Ostaska",
    author_email="marcoan@ymail.com",
    description="get information about a given month",
    long_description="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
