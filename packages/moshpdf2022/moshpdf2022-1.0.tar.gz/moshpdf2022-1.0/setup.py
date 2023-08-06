import setuptools
from pathlib import Path

setuptools.setup(
    name="moshpdf2022",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"]) # exclude folders
)