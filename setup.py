# -*- coding: utf-8 -*-

from setuptools import setup

__author__ = "Hendrikx ITC"

setup(
    name="minerva_harvest_csv",
    version="1.0.0",
    description=__doc__,
    author=__author__,
    install_requires=["minerva"],
    packages=["minerva_harvest_csv"],
    package_dir={"": "src"},
    entry_points={
        "minerva.harvest.plugins": ["csv = minerva_harvest_csv:Plugin"],
        "minerva.data_generator": ["csv = minerva_harvest_csv.generate:generate"]
    }
)
