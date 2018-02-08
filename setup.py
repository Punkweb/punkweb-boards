import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django_boards",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    description='Django forum boards with bbcode support.',
    long_description=README,
    url='https://punkweb.us/',
    author='Jordan Price',
    author_email='Jordan Price <pricejordan@outlook.com>',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    setup_requires=['django>=1.8'],
    install_requires=open('requirements.txt').readlines(),
)
