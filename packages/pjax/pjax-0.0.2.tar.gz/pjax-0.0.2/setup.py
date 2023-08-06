import codecs
import os.path

import setuptools


# Get the package's version number of the __init__.py file
def read(rel_path: str) -> str:
    """Read the file located at the provided relative path."""
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    """Get the package's version number.
    We fetch the version  number from the `__version__` variable located in the
    package root's `__init__.py` file. This way there is only a single source
    of truth for the package's version number.
    """
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


folder = os.path.dirname(__file__)

req_path = os.path.join(folder, "requirements.txt")
install_requires = []
if os.path.exists(req_path):
    with open(req_path) as fp:
        install_requires = [line.strip() for line in fp]

readme_path = os.path.join(folder, "README.md")
readme_contents = ""
if os.path.exists(readme_path):
    with open(readme_path) as fp:
        readme_contents = fp.read().strip()


setuptools.setup(
    name="pjax",
    author="lawortsmann",
    url="https://github.com/lawortsmann/pjax",
    version=get_version("pjax/__init__.py"),
    description="Probability distributions for JAX",
    long_description=readme_contents,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    requires_python=">=3.7",
)
