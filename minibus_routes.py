import requests
import itertools
import logging
from io import StringIO
from minibus_stops import MinibusStop
from minibus_stops import MinibusStops
from dataclasses import dataclass
from typing import NamedTuple
from typing import List
from timetable import Timetable
from utility import handle_response

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class RouteID(NamedTuple):
    route_number: str
    type: str


@dataclass
class MinibusRoute:
    name: str
    stops: List[MinibusStop]
    timetable: Timetable


class MinibusRoutes(dict):
    routes_url = 'https://marsruti.lv/rigasmikroautobusi/bbus/routes.txt'

    key_translation = {'routenum': 'route_number',
                       'routename': 'route_name',
                       'routestops': 'route_stops',
                       'routetype': 'route_type'}

    def __init__(self):
        super().__init__()
        with requests.get(self.routes_url) as response:
            content = response.content.decode('utf-8-sig')

            handle_response(response)

            with StringIO(content) as sting_buffer:
                header_row = sting_buffer.readline().lower().split(';')
                _ = sting_buffer.readline(), sting_buffer.readline()  # throw away unnecessary lines

                fieldnames = [field if (field not in self.key_translation) else self.key_translation[field]
                              for field in header_row]

                stops = MinibusStops()

                last_route_number = None
                for column_values, timetable in itertools.zip_longest(*[sting_buffer] * 2):
                    timetable = timetable.strip()
                    column_values = column_values.split(';')

                    route_data = dict(zip(fieldnames, column_values))

                    route_number = route_data['route_number']
                    route_type = route_data['route_type']
                    route_name = route_data['route_name']
                    route_stops = [route_stop
                                   for route_stop in route_data['route_stops'].split(',')
                                   if len(route_stop) > 0]

                    if len(route_number) == 0:
                        route_number = last_route_number

                    route_stops = [stops[route_stop] for route_stop in route_stops]

                    route_id = RouteID(route_number=route_number, type=route_type)
                    route = MinibusRoute(name=route_name, stops=route_stops, timetable=Timetable(timetable))
                    last_route_number = route_number
                    self[route_id] = route
