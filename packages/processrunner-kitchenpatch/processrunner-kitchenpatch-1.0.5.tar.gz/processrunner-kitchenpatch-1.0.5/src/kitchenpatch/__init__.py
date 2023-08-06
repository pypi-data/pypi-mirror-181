# -*- coding: utf-8 -*-
from kitchenpatch.kitchenpatch import getwriter

# Define version variable
from importlib_metadata import version, packages_distributions, PackageNotFoundError

try:
    packages = packages_distributions()
    package_name = packages[__name__][0]
    __version__ = version(package_name)
except (PackageNotFoundError, KeyError):
    # package is not installed
    pass