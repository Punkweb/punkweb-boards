import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="punkweb_boards",
    version="0.0.12",
    packages=["punkweb_boards"],
    include_package_data=True,
    description="Django forum boards with bbcode support.",
    long_description=README,
    url="https://punkweb.net/board/",
    author="Punkweb",
    author_email="Punkweb <punkwebnet@gmail.com>",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: Forums",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    setup_requires=["django>=3.2"],
    install_requires=open("requirements.txt").readlines(),
)
