import os
import re
from setuptools import setup


description = "Flask-PynamoDB is an extensio for integrating with PynamoDB"

with open("flask_pynamodb/__init__.py") as init_file:
    version = re.search(r'__version__ = "(.*?)"', init_file.read()).group(1)

with open("README.md") as readme_file:
    long_description = readme_file.read()

setup(
    name="Flask-PynamoDB",
    version=version,
    url="https://github.com/bl4ckst0ne/flask-pynamodb",
    license="MIT",
    author="bl4ckst0ne",
    author_email="bl4ckst0ne1@gmail.com",
    description=description,
    long_description=long_description,
    packages=["flask_pynamodb"],
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=["Flask>=1.1.2", "pynamodb>=4.3.3"],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
