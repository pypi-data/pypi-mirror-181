# -*- coding: utf-8 -*-

# =================================================================================
# Authors:
#       Jon Perry
#       Joshua Oliveira
# Email:
#       jon@jonperry.dev
#       Joshua.oliveiramartin@gmail.com
# =================================================================================

from pathlib import Path
from setuptools import setup, find_packages

try:
    version_path = Path(__file__).parent / "walle" / "VERSION"
    version = version_path.read_text().strip()
except FileNotFoundError:
    version = "0.0.0"

REQUIREMENTS = [
    "discord==2.1.0",
    "black==22.10.0",
    "flake8==6.0.0",
    "pre-commit==2.20.0",
]


def setup_package():
    setup(
        name="discord-walle",
        version=version,
        description="General Discord Utility Bot",
        author=[
            "Jon Perry",
            "Josh Oliveira",
        ],
        license="Unlicense",
        packages=find_packages(),
        include_package_data=True,
        install_requires=REQUIREMENTS,
        python_requires="~=3.8",
    )


if __name__ == "__main__":
    setup_package()
