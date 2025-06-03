#!/usr/bin/env python3
"""
Setup script for Dungeon Master.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() if (this_directory / "README.md").exists() else ""

# Version info - keeping it simple for now
version = {
    "__version__": "0.3.1",
    "__author__": "Dungeon Master Team",
    "__description__": "Context-tracking pre-commit tool for Cursor integration"
}

setup(
    name="cursor-dungeon-master",
    version=version.get("__version__", "0.1.0"),
    author=version.get("__author__", "Dungeon Master Team"),
    author_email="contact@dungeonmaster.dev",
    description=version.get("__description__", "Context-tracking pre-commit tool for maintaining documentation"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dungeon-master",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies for core functionality
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "dm=dungeon_master.cli:main",
            "dungeon-master=dungeon_master.cli:main",
        ],
    },
    include_package_data=True,
    keywords="documentation git pre-commit context tracking",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/dungeon-master/issues",
        "Source": "https://github.com/yourusername/dungeon-master",
    },
)
