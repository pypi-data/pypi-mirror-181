from pathlib import Path

from lib.common._version import __version__
from setuptools import find_namespace_packages, setup

this_directory = Path(__file__).parent
readme_content = (this_directory / "README.md").read_text()

dependencies = [
    "appdirs",
    "wheel>=0.31.0",
    "boto3>=1.20.15",
    "tensorflow-cpu",
    "click>=8.0.1",
    "questionary>=1.10.0",
    "torch",
    "torchvision",
]

setup(
    name="autumn8",
    version=__version__,
    author="Autumn8",
    author_email="marcink@radcode.co",  # TODO use some common support mail from autumn8?
    install_requires=dependencies,
    setup_requires=dependencies,
    packages=find_namespace_packages(include=["lib.*"]),
    description="Utilities to export models to the autumn8.ai service",
    long_description=readme_content,
    long_description_content_type="text/markdown; charset=UTF-8; variant=GFM",
    entry_points={
        "console_scripts": [
            "autumn8-cli=lib.cli.main:main",
        ],
    },
)
