from setuptools import setup, find_packages


# All reusable metadata should go here.

name: str = "pyjoptional"
description: str = "Java-like Optional type for Python 3.9+"
author: str = "Emanuele Uliana"
license: str = "GNU3"
classifiers: list = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3 :: Only",
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
]
dependencies: list = ["wheel"]

# End of metadata

setup(
    name=name,
    version="1.0.0",
    description=description,
    author=author,
    license=license,
    packages=find_packages(),
    include_package_data=True,
    install_requires=dependencies,
    classifiers=classifiers
)
