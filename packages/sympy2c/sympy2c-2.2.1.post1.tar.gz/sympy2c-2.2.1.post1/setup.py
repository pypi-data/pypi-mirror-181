#!/usr/bin/env python
from setuptools import setup

from pathlib import Path

long_description = (
    Path("README.rst").read_text() + 3 * "\n" + Path("HISTORY.rst").read_text()
)

setup(
    long_description=long_description,
    long_description_content_type="text/x-rst; charset=UTF-8",
)
