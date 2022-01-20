from setuptools import find_packages, setup

with open("requirements.txt", "r", encoding="utf-8") as f:
    requires = [x.strip() for x in f if x.strip()]

setup(name="src", packages=find_packages(), version="0.1.0", install_requires=requires)