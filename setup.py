# -*- coding: utf-8 -*-

from setuptools import setup

__author__ = "Hendrikx ITC"

setup(
    name="minerva-harvest-csv-luftdaten",
    version="1.0.1",
    description=__doc__,
    author=__author__,
    author_email='info@hendrikx-itc.nl',
    python_requires='>=3.5',
    install_requires=["minerva-etl>=5.0.0.dev2"],
    packages=["minerva_harvest_csv_luftdaten"],
    package_dir={"": "src"},
    entry_points={
        "minerva.harvest.plugins": ["csv_luftdaten = minerva_harvest_csv_luftdaten:Plugin"],
        "minerva.data_generator": ["csv_luftdaten = minerva_harvest_csv_luftdaten.generate:generate"]
    }
)
