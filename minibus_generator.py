import time
import logging
from dataclasses import dataclass
from geolocation import Geolocation
import requests
import glob
import pathlib
from utility import handle_response

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


@dataclass
class Minibus:
    route_number: str
    location: Geolocation
    speed: int
    heading: int
    car_id: str

    def __init__(self, raw_minibus: str):
        self.route_number, longitude, latitude, self.speed, self.heading, self.car_id = raw_minibus.split(',')[1:-1]

        self.route_number, self.speed, self.heading = self.route_number, int(self.speed), int(self.heading)

        longitude, latitude = int(longitude) / 1000000, int(latitude) / 1000000
        self.location = Geolocation(latitude=latitude, longitude=longitude)


class MinibusGenerator:

    def __init__(self, debug=False):
        self.session = requests.session()
        self.minibus_url = 'http://marsruti.lv/rigasmikroautobusi/gps.txt?{}'

        if debug:
            self.minibus_archive = glob.glob('gps/*.txt')
            self.minibus_archive = sorted(self.minibus_archive, key=lambda path: pathlib.Path(path).name)
            self.get_minibuses = self.get_minibuses(self.get_minibuses_archive)
        else:
            self.get_minibuses = self.get_minibuses(self.get_minibuses_online)

    @staticmethod
    def get_minibuses(minibus_retriever):
        def get_minibuses():
            timestamp, minibuses = minibus_retriever()
            return int(timestamp), {minibus.car_id: minibus
                                    for minibus in (Minibus(minibus)
                                                    for minibus in minibuses
                                                    if len(minibus) > 0)}

        return get_minibuses

    def get_minibuses_archive(self):
        file_name = self.minibus_archive.pop(0)

        def minibus_generator(file):
            logger.debug('file: {}'.format(file))
            with open(file, mode='r', encoding='utf-8') as archive_gps:
                for line in archive_gps:
                    yield line

        current_unix_timestamp = pathlib.Path(file_name).stem
        minibuses = minibus_generator(file_name)
        return current_unix_timestamp, minibuses

    def get_minibuses_online(self):
        current_unix_timestamp = time.time()
        minibus_url = self.minibus_url.format(str(round(current_unix_timestamp, 3)).replace('.', ''))

        logger.debug('timestamp: {}'.format(current_unix_timestamp))

        with self.session.get(minibus_url) as response:
            handle_response(response)

            minibuses = response.iter_lines(decode_unicode=True, delimiter='\n')

            return current_unix_timestamp, minibuses


def main():
    minibus_generator = MinibusGenerator(debug=True)
    _, minibuses = minibus_generator.get_minibuses()
    for minibus in minibuses:
        print(minibus)


if __name__ == '__main__':
    main()
