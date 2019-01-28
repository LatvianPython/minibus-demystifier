from collections import namedtuple
import requests
from geolocation import Geolocation
from dataclasses import dataclass
from io import StringIO
from contextlib import suppress
import csv
from typing import List
import logging
from utility import handle_response

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


@dataclass
class MinibusStop:
    location: Geolocation
    name: str


ClosestStop = namedtuple(typename='ClosestStop', field_names=['stop_index', 'stop'])


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


# fixme: this seems pretty bad, especially the use in tracking
def closest_stop(minibus, stops: List[MinibusStop]):
    closest, distance_to_closest = min([(ClosestStop(index, stop), minibus.location - stop.location)
                                        for index, stop in enumerate(stops)],
                                       key=lambda a: a[1])
    return closest

