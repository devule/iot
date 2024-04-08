from csv import DictReader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
from domain.parking import Parking
import config


class FileDatasource:
    def __init__(
        self,
        accelerometer_filename: str,
        gps_filename: str,
        parking_filename: str,
    ) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename
        self.accelerometer_file = None
        self.gps_file = None
        self.parking_file = None
        self.accelerometer_csv = None
        self.gps_csv = None
        self.parking_csv = None

    def read(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""
        if not self.accelerometer_csv or not self.gps_csv or not self.parking_csv:
            raise Exception("Files are not open.")

        try:
            accelerometer_row = next(self.accelerometer_csv)
            gps_row = next(self.gps_csv)
            parking_row = next(self.parking_csv)
        except StopIteration:
            self.stopReading()
            self.startReading()
            accelerometer_row = next(self.accelerometer_csv)
            gps_row = next(self.gps_csv)
            parking_row = next(self.parking_csv)

        accelerometer_data = Accelerometer(accelerometer_row.get('x'), accelerometer_row.get('y'), accelerometer_row.get('z'))
        gps_data = Gps(gps_row.get('longitude'), gps_row.get('latitude'))
        parking_data = Parking(parking_row.get('empty_count'), Gps(parking_row.get('longitude'), parking_row.get('latitude')))

        return AggregatedData(
            accelerometer_data,
            gps_data,
            parking_data,
            datetime.now(),
            config.USER_ID,
        )

    def startReading(self, *args, **kwargs):
        self.accelerometer_file = open(self.accelerometer_filename, 'r')
        self.gps_file = open(self.gps_filename, 'r')
        self.accelerometer_csv = DictReader(self.accelerometer_file)
        self.gps_csv = DictReader(self.gps_file)
        self.parking_file = open(self.parking_filename, 'r')
        self.parking_csv = DictReader(self.parking_file)

    def stopReading(self, *args, **kwargs):
        if self.accelerometer_file:
            self.accelerometer_file.close()
        if self.gps_file:
            self.gps_file.close()
        if self.parking_file:
            self.parking_file.close()
