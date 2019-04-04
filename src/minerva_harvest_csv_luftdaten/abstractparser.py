import datetime
import csv

from minerva.harvest.plugin_api_trend import HarvestParserTrend
from minerva.storage.trend.datapackage import DataPackage, DataPackageType
from minerva.storage.trend.granularity import create_granularity
from minerva.directory.helpers import dns_to_entity_ids
from minerva.directory.distinguishedname import entity_type_name_from_dn


class CsvParser(HarvestParserTrend):
    # abstract class for creating data from csv
    def __init__(self, config):
        self.config = config
        # the following can (in the case of idvar and datavars: should) be overwritten in the setup of child classes
        self.idvar = None # name on the csv for the name
        self.idname = "ident" # name for Minerva of the entity type
        self.datavars = {} # name on the csv to trendname
        self.changedata = {} # function to apply to the data
        self.datevar = None # name of the variable that contains the date
        self.timeformats = ["%Y-%m-%d %X"] # datetime format used, if more than one specified they are tried in sequence
        self.timeshift = datetime.timedelta(0) # by how much should the date be changed
        self.delimiter = ";"
        self.quotechar = '"'
        self.startstring = None # if this has a value, the first line is considered to be the one following the one that contains this string (as a field by itself)
        self.allowempty = [] # data fields that are allowed to be empty. Please include only string fields
        self.setup()

    def setup(self):
        # this should be overwritten in child classes to create an actual parser
        raise NotImplementedError

    def changeddata(self, datavar, value):
        # the actual data when value is given for datavar
        if datavar in self.changedata:
            return str(self.changedata[datavar](value))
        else:
            return value

    def load_packages(self, stream, name):
        csvreader = csv.reader(stream, delimiter = self.delimiter, quotechar = self.quotechar)
        rows_by_timestamp = {}
        header = None
        self.active = not self.startstring
        for measurement in csvreader:
            if not self.active:
                # we are not yet in the part of the csv we have to look at
                self.active = self.startstring in measurementx
            elif not header:
                # first line, containing the header information
                header = measurement
            else:
                # actual data row
                rowname = None
                timestamp = None
                trend_row = []

                for (datatype, value) in zip(header, measurement):
                    value = self.changeddata(datatype, value)
                    if value == '' and datatype not in self.allowempty:
                        value = None
                    if value == '': value = None
                    if datatype == self.datevar:
                        for format in self.timeformats:
                            try:
                                timestamp = datetime.datetime.strptime(value, format) + self.timeshift
                                break
                            except ValueError:
                                continue
                        else:
                            raise ValueError("No applicable timeformat")
                    elif datatype == self.idvar:
                        rowname = value
                    elif datatype in self.datavars:
                        trend_row.append(value)
                if not rowname and timestamp:
                    # insufficient data to create a datarow
                    continue

                rows = rows_by_timestamp.get(timestamp)
                if not rows:
                    rows = []
                    rows_by_timestamp[timestamp] = rows

                row_ident = '{}={}'.format(self.idname, rowname)
                rows.append((row_ident, trend_row))

        trend_names = [self.datavars[name] for name in [name for name in header if name in self.datavars]]

        package_type = DataPackageType(DnRef(), entity_type_name_from_dn)

        for timestamp, rows in rows_by_timestamp.items():
            print("{}: {}".format(timestamp, rows))
            yield DataPackage(
                package_type,
                create_granularity('1 day'),
                timestamp,
                trend_names,
                rows
            )


class DnRef:
    def map_to_entity_ids(self, dns):
        def map_to(cursor):
            return dns_to_entity_ids(cursor, dns)

        return map_to


def entity_type_from_dn(data_package):
    first_row = data_package.rows[0]

    dn, timestamp, values = first_row

    return entity_type_name_from_dn(dn)
