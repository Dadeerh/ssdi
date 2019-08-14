from setuptools import setup, find_packages
from pkg_resources import resource_string

long_desc = str(resource_string(__name__, "Readme.md"))

setup(
    name="ssdi",
    version="0.1",
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