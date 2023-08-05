import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sharpfed",
    version="0.0.3",
    author="wangshuo",
    author_email="shuowan16@163.com",
    description="Fast and easy federated learning framework based on Tensorflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WhatIsSurprise/SharpFed",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='<=3.8.10',
)