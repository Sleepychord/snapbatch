# Copyright (c) Ming Ding.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from pathlib import Path

from setuptools import find_packages, setup

def _requirements():
    return Path("requirements.txt").read_text()

setup(
    name="snapbatch",
    version=0.2,
    description="`snapbatch` is a replacement of `sbatch` to create a snapshot of current working directory, and submit the command to `sbatch`.",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    install_requires=_requirements(),
    entry_points={"console_scripts": ["snapbatch = snapbatch.cli:main"]},
    packages=find_packages(),
    url="",
    author="Ming Ding",
    author_email="mingding.thu@gmail.com",
    scripts={"snapbatch_purge"},
    include_package_data=True,
    python_requires=">=3.5",
    license="MIT license"
)