from setuptools import setup
from setuptools import find_packages

VERSION = "1.1.1"

setup(
    name="carapiparser",
    version=VERSION,
    description="parse car api excel config",
    long_description=open("README.md", "r").read(),
    packages=find_packages(),
    author="zoulx",
    author_email="894919296@qq.com",
    url="https://github.com/chinaZoulx",
    license="MIT",
    platforms=["all"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        "xlrd>=1.2.0",
    ],
)
