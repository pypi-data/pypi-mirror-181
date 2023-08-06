import os
import re
import subprocess
import sys

from setuptools import setup


def get_version(package: str) -> str:
    """Return version of the package."""
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), package, "__init__.py"
    )
    with open(path, "r") as file:
        source = file.read()
    m = re.search(r'__version__ = ["\'](.+)["\']', source)
    if m:
        return m.group(1)
    else:
        return "0.0.0"


def get_packages(package):
    """Return root package and all sub-packages."""
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


with open('README.md') as readme_file:
    readme = readme_file.read()


setup(
    name="mkapi-fix-coz",
    version=get_version("mkapi"),
    description="An Auto API Documentation tool.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/cityofzion/mkapi",
    author="coz",
    author_email="python@coz.io",
    license="MIT",
    packages=get_packages("mkapi") + ["mkapi/templates", "mkapi/theme"],  # FIXME
    include_package_data=True,
    install_requires=["markdown", "jinja2"],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": ["mkapi = mkapi.main:cli"],
        "mkdocs.plugins": ["mkapi = mkapi.plugins.mkdocs:MkapiPlugin"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Documentation",
    ],
)
