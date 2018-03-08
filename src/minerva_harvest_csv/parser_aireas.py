import datetime

try:
    from minerva_harvest_csv.abstractparser import CsvParser
except ModuleNotFoundError:
    from abstractparser import CsvParser
    
class Parser(CsvParser):
    def setup(self):
        self.idvar = "id"
        self.idname = "airbox"
        self.datavars = {
            "PM1": "PM1",
            "PM10": "PM10",
            "PM25": "PM25",
            "WBGT": "WBGT",
            "UFP": "UFP",
            "Ozon": "Ozon",
            "NO2": "NO2",
            "Temp": "Temp",
            "AmbTemp": "AmbTemp",
            "RelHum": "RelHum",
            "AmbHum": "AmbHum",
            "lat": "GPS.lat",
            "lon": "GPS.lon"
            }
        self.datevar = "measured"
        self.startstring = "MEASUREMENTS"
        self.changedata = {
            "lat": lambda x: float(x) * 100,
            "lon": lambda x: float(x) * 100
            }
        self.timeshift = datetime.timedelta(seconds=5)

