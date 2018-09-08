import os
from setuptools import setup, find_packages

setup(
    name = "python_static_analyzer",
    version = "0.0.0",
    description = ("CMU CHIMPS static analyzer for android APKs"),
    license = "BSD",
    packages=find_packages(),
    install_requires=["mysqlclient", "numpy", "pandas", "pymongo"]
)
