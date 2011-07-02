#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError as ie:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup

# Startup
appname = "assemblage"
appversion = "0.1"

setup(
    name = appname,
    version = appversion,
    url='https://github.com/pmatiello/assemblage',

    author = "Pedro Matiello",
    author_email='pmatiello@gmail.com',
    
    description = "A small Python framework for building objects in dependency-injection style.",
    long_description = "A small Python framework for building objects in dependency-injection style.",
    keywords = "",
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
    ],
    license = "MIT",
    
    py_modules = ["assemblage"],
    include_package_data = True,
    zip_safe = True,
)
