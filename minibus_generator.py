import time
import logging
from dataclasses import dataclass
from geolocation import Geolocation
import requests
import glob
from utility import to_datetime
import pathlib
from datetime import datetime
from typing import Dict
from utility import handle_response

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


@dataclass
class Minibus:
    route_number: str
    location: Geolocation
    speed: int
    heading: int


class MinibusGenerator:

    def __init__(self, debug=False):
        self.session = requests.session()
        self.minibus_url = 'http://marsruti.lv/rigasmikroautobusi/gps.txt?{}'

        if debug:
            self.minibus_archive = glob.glob('gps/*.txt')
            self.minibus_archive = sorted(self.minibus_archive, key=lambda path: pathlib.Path(path).name)
            self.get_minibuses = self.get_minibuses(self.__get_minibuses_archive)
        else:
            self.get_minibuses = self.get_minibuses(self.__get_minibuses_online)

    @staticmethod
    def __parse_minibus(minibus: str):
        route_number, longitude, latitude, speed, heading, car_id = minibus.split(',')[1:-1]

        route_number, speed, heading = route_number, int(speed), int(heading)

        longitude, latitude = int(longitude) / 1000000, int(latitude) / 1000000
        location = Geolocation(latitude=latitude, longitude=longitude)

        return car_id, Minibus(route_number=route_number, location=location, speed=speed, heading=heading)

    def get_minibuses(self, minibus_retriever) -> (datetime, Dict[str, Minibus]):
        def get_minibuses():
            timestamp, minibuses = minibus_retriever()
            logger.debug('timestamp: {}'.format(timestamp))
            return (to_datetime(timestamp),
                    {car_id: minibus
                     for car_id, minibus in (self.__parse_minibus(minibus)
                                             for minibus in minibuses
                                             if len(minibus) > 0)})

        return get_minibuses

    def __get_minibuses_archive(self):
        file_name = self.minibus_archive.pop(0)

        def minibus_generator(file):
            logger.debug('file: {}'.format(file))
            with open(file, mode='r', encoding='utf-8') as archive_gps:
                for line in archive_gps:
                    yield line

        current_unix_timestamp = pathlib.Path(file_name).stem
        minibuses = minibus_generator(file_name)
        return current_unix_timestamp, minibuses

    def __get_minibuses_online(self):
        current_unix_timestamp = time.time()
        minibus_url = self.minibus_url.format(str(round(current_unix_timestamp, 3)).replace('.', ''))

        logger.debug('timestamp: {}'.format(current_unix_timestamp))

        with self.session.get(minibus_url) as response:
            handle_response(response)

            minibuses = response.iter_lines(decode_unicode=True, delimiter='\n')

            return current_unix_timestamp, minibuses


def main():
    minibus_generator = MinibusGenerator(debug=True)
    current_time, minibuses = minibus_generator.get_minibuses()

    print(current_time.second + current_time.hour * 60)
    for minibus in [item
                    for i, item in enumerate(minibuses.items())
                    if i < 5]:
        print(minibus)


if __name__ == '__main__':
    main()