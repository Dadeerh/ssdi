import os
from setuptools import setup, find_packages
from pkg_resources import resource_string

long_desc = open(os.path.join(os.path.dirname(__file__),"Readme.md")).read()

setup(
    name="ssdi",
    version="0.1.1",
    scripts=["ssdi.py"],
    package_data={
        "":["*.md"]
    },
    author="Dadeerh",
    author_email="dadeerh91@gmail.com",
    description="Super Simple Dependency Injector",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    keywords="dependency injection injector di super simple",
    url="",
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ]
)