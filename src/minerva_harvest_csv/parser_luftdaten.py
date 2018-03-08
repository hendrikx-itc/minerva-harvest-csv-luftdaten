from abstractparser import CsvParser

class Parser(CsvParser):
    def setup(self):
        self.idvar = "sensor_id"
        self.idname = "sensor"
        self.datavars = {
            "sensor_type": "sensor_type",
            "location": "location",
            "lat": "GPS.lat",
            "lon": "GPS.lon",
            "P1": "P1",
            "durP1": "durP1",
            "ratioP1": "ratioP1",
            "P2": "P2",
            "durP2": "durP2",
            "ratioP2": "ratioP2"
            }
        self.datevar = "timestamp"
        self.timeformat = "%Y-%m-%dT%X.%f%z"
