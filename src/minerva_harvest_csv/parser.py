import csv
import datetime

from minerva.harvest.plugin_api_trend import HarvestParserTrend
from minerva.storage.trend.datapackage import DefaultPackage
from minerva.storage.trend.granularity import create_granularity


class Parser(HarvestParserTrend):
    def __init__(self, config):
        self.config = config

    def load_packages(self, stream, name):
        csvreader = csv.reader(stream, delimiter=',')

        header = next(csvreader)

        rows = []

        def get_ident(row):
            return 'unknown={}'.format(row[0])

        for row in csvreader:
            rows.append((get_ident(row), row))

        yield DefaultPackage(create_granularity('1 day'), datetime.datetime.utcnow(), header, rows)

