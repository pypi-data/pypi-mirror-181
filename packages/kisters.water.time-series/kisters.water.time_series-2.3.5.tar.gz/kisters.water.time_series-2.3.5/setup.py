from codecs import open
from os import path

from setuptools import find_namespace_packages, setup

# Get the long description from README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="kisters.water.time_series",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    python_requires=">=3.9",
    description="KISTERS WATER Time Series Access library",
    long_description=long_description,
    url="https://gitlab.com/kisters/kisters.water.time_series",
    author="Alberto Sabater",
    author_email="alberto.sabatermorales@kisters.de",
    license="LGPL",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="kisters water time series",
    packages=find_namespace_packages(include=["kisters.*"]),
    package_data={"": ["py.typed"]},
    zip_safe=False,
    install_requires=["orjson", "pandas", "pyarrow", "pydantic"],
    extras_require={
        "test": [
            "pytest",
            "pytest-asyncio",
        ],
        "docs": ["sphinx", "sphinx_rtd_theme"],
    },
)
