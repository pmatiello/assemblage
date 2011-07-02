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
    author = "Pedro Matiello",
    py_modules = ["assemblage"],
    author_email = "pmatiello@gmail.com",
    description = "A small Python framework for building objects in dependency-injection style.",
    license = "MIT",
    keywords = "",
    url = "https://github.com/pmatiello/luminescence",
    long_description = "A small Python framework for building objects in dependency-injection style.",
    include_package_data = True,
    zip_safe = True,
)
