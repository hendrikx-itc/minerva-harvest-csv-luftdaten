import csv
import datetime
from operator import itemgetter

from minerva.harvest.plugin_api_trend import HarvestParserTrend
from minerva.storage import datatype
from minerva.storage.trend.datapackage import DataPackage, DataPackageType, \
    EntityDnRef, from_first_dn
from minerva.storage.trend.granularity import create_granularity
from minerva.storage.trend.trend import Trend

"""
config = {
    "header": "first_line",
    "delimiter": ",",
    "timestamp": {
        "from_column": "meas_date"
    },
    "identifier": {
        "format": "node={node}"
    }
    "columns": [
        {
            "name": "node",
            "data_type": "text"
        },
        {
            "name": "meas_date",
            "data_type": "timestamp with time zone"
        },
        {
            "name": "bytes_up",
            "data_type": "integer"
        },
        {
            "name": "bytes_down",
            "data_type": "integer"
        }
    ]
}
"""


def create_timestamp_extractor(conf):
    if "from_column" in conf:
        return itemgetter(conf['from_column'])
    else:
        raise Exception('Configuration error')


class Parser(HarvestParserTrend):
    def __init__(self, config):
        self.config = config

    def load_packages(self, stream, name):
        extract_timestamp = create_timestamp_extractor(self.config.get('timestamp'))

        trend_descriptors = [
            Trend.Descriptor(column['name'], column['data_type'], '')
            for column in self.config['columns']
        ]
        column_parsers = {
            column['name']: datatype.registry[column['data_type']].string_parser(column.get('config'))
            for column in self.config['columns']
        }

        csv_reader = csv.reader(
            stream,
            delimiter=self.config.get('delimiter', ',')
        )

        header_config = self.config.get('header', 'first_line')

        if header_config == 'first_line':
            header = next(csv_reader)
        elif header_config == 'from_columns_config':
            header = [column['name'] for column in self.config['columns']]
        else:
            raise Exception(
                'Unrecognized header config: {}'.format(header_config)
            )

        ordered_parsers = [
            column_parsers[column_name] for column_name in header
        ]

        build_identifier = identifier_builder(self.config['identifier'])

        def process_row(row):
            values = [
                parser(value_text)
                for parser, value_text in zip(ordered_parsers, row)
            ]

            values_dict = dict(zip(header, values))

            return (
                build_identifier(values_dict),
                extract_timestamp(values_dict),
                values
            )

        data_package_type = DataPackageType(EntityDnRef, from_first_dn)

        yield DataPackage(
            data_package_type,
            create_granularity('1 day'),
            trend_descriptors, list(map(process_row, csv_reader))
        )


def identifier_builder(config):
    def build_identifier(row_dict):
        return config['format'].format(**row_dict)

    return build_identifier
