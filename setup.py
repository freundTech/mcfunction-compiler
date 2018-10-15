from setuptools import setup, find_packages

from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="mcfunction_compiler",
    version="0.1",
    description="Compile high level code to .mcfunction files",
    long_description=long_description,
    author="Adrian Freund",
    author_email="mail@freundtech.com",
    url="https://github.com/freundTech/mcfunction-compiler",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="minecraft compiler mcfunction",
    packages=find_packages(include="mcfunction_compiler"),
    install_requires=["lark"],
    python_requires=">=3",
    entry_points={
        "console_scripts": ["mcfc=mcfunction_compiler.__main__.main"]
    },
    test_suite="test"
)