# -*- coding: utf-8 -*-

from setuptools import setup

__author__ = "Hendrikx ITC"

setup(
    name="minerva-harvest-csv",
    version="1.0.1",
    description=__doc__,
    author=__author__,
    author_email='info@hendrikx-itc.nl',
    python_requires='>=3.5',
    install_requires=["minerva-etl>=5.0.0.dev2"],
    packages=["minerva_harvest_csv"],
    package_dir={"": "src"},
    entry_points={
        "minerva.harvest.plugins": ["csv = minerva_harvest_csv:Plugin"],
        "minerva.data_generator": ["csv = minerva_harvest_csv.generate:generate"]
    }
)
