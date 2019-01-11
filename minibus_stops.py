import requests
from geolocation import Geolocation
from dataclasses import dataclass
from io import StringIO
from contextlib import suppress
import csv
import logging
from utility import handle_response

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


@dataclass
class MinibusStop:
    location: Geolocation
    name: str


def gtfs_stops():
    with open('gtfs/stops.txt', mode='r', encoding='utf-8-sig', newline='') as file:
        delimiter = ','
        fieldnames = file.readline().strip().split(delimiter)
        stop_reader = csv.DictReader(file, delimiter=delimiter, quotechar='"', fieldnames=fieldnames)

        for row in stop_reader:
            stop_id, name, longitude, latitude = row['stop_id'], row['stop_name'], row['stop_lon'], row['stop_lat']
            longitude, latitude = float(longitude), float(latitude)
            location = Geolocation(longitude=longitude, latitude=latitude)
            yield stop_id, MinibusStop(location=location, name=name)


def online_stops():
    stops_url = 'https://marsruti.lv/rigasmikroautobusi/bbus/stops.txt'
    with requests.get(stops_url) as response:
        content = response.content.decode('utf-8-sig')

        handle_response(response)

        with StringIO(content) as csv_data:
            delimiter = ';'
            fieldnames = csv_data.readline().strip().lower().split(delimiter)
            stop_reader = csv.DictReader(csv_data, delimiter=delimiter, fieldnames=fieldnames)

            for row in stop_reader:
                stop_id, name, longitude, latitude = row['id'], row['name'], row['lng'], row['lat']
                longitude, latitude = int(longitude) / 100000, int(latitude) / 100000
                location = Geolocation(longitude=longitude, latitude=latitude)
                yield stop_id, MinibusStop(location=location, name=name)


class MinibusStops(dict):

    def __init__(self):
        super().__init__()

        stops_from_gtfs = {stop_id: stop for stop_id, stop in gtfs_stops()}
        for stop_id, stop in online_stops():
            if stop.name is None:
                with suppress(KeyError):
                    stop.name = stops_from_gtfs[stop_id].name
            self[stop_id] = stop


def main():
    minibus_stops = MinibusStops()

    for stop_id, stop in minibus_stops.items():
        print(stop_id, stop)


if __name__ == '__main__':
    main()
