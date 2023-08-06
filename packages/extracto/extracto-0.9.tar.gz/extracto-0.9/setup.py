from setuptools import setup
import os

VERSION = "0.9"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="extracto",
    description="Extract Python dicts from HTML files, fast.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Colin Dellow",
    url="https://github.com/cldellow/extracto",
    project_urls={
        "Issues": "https://github.com/cldellow/extracto/issues",
        "CI": "https://github.com/cldellow/extracto/actions",
        "Changelog": "https://github.com/cldellow/extracto/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["extracto"],
    install_requires=["selectolax"],
    extras_require={"test": ["pytest", "pytest-watch", "wheel", "pytest-skip-slow", "pytest-profiling"]},
    python_requires=">=3.7",
)
