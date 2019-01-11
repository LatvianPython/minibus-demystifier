import time
import logging
from dataclasses import dataclass
from geolocation import Geolocation
import requests

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


@dataclass
class Minibus:
    route_number: int
    location: Geolocation
    speed: int
    heading: int
    car_id: str

    def __init__(self, raw_minibus: str):
        self.route_number, longitude, latitude, self.speed, self.heading, self.car_id = raw_minibus.split(',')[1:-1]

        self.route_number, self.speed, self.heading = int(self.route_number), int(self.speed), int(self.heading)

        longitude, latitude = int(longitude) / 1000000, int(latitude) / 1000000
        self.location = Geolocation(latitude=latitude, longitude=longitude)


class Minibuses:

    def __init__(self):
        self.session = requests.session()
        self.minibus_url = 'http://marsruti.lv/rigasmikroautobusi/gps.txt?{}'

    def __iter__(self):
        current_unix_timestamp = str(round(time.time(), 3)).replace('.', '')
        minibus_url = self.minibus_url.format(current_unix_timestamp)

        logger.debug('timestamp: {}'.format(current_unix_timestamp))

        with self.session.get(minibus_url) as response:

            if response.status_code == 200:
                logger.debug('response status: {}, length: {}'.format(response.status_code, len(response.content)))
            else:
                logger.critical(
                    'request failed with {}, content = "{}", headers = "{}", cookies = "{}"'.format(
                        response.status_code,
                        response.content,
                        response.headers,
                        response.cookies)
                )
                response.raise_for_status()

            minibuses = response.iter_lines(decode_unicode=True, delimiter='\n')

            return (Minibus(minibus)
                    for minibus in minibuses
                    if len(minibus) > 0)


def main():
    minibuses = Minibuses()

    for minibus in minibuses:
        print(minibus)


if __name__ == '__main__':
    main()
