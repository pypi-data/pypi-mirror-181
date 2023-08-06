from pathlib import Path
from setuptools import setup, find_packages
import re
import os


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

DESCRIPTION = "A python framework to work with biomedical signals."
PACKAGE_NAME = "pybiosig"
AUTHOR = "Alejandro Alcaine, PhD"
EMAIL = "lalcaine@usj.es"
GITHUB_URL = "https://github.com/aalcaineo/PyBiosig"

with open(os.path.join(this_directory,PACKAGE_NAME,"__init__.py"), "r") as f:
    version = ""
    while not version:
        version = re.findall('\t*\s*^__version__\s*=\s*"(\d\.\d\.\d)"\n+', f.readline())

setup(
    name=PACKAGE_NAME,
    packages=find_packages(exclude=['*tests*']),
    version=version[0],
    license="GNU General Public License v3.0",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=GITHUB_URL,
    keywords=["Signal", "Reading","Biomedical"],
    install_requires=["bokeh>=3.0.3","matplotlib>=3.6.2","pandas>=1.5.2","numpy>=1.23.5"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
    ],
    zip_safe=False,
)
