from minibus_generator import MinibusGenerator
from minibus_stops import MinibusStop
from typing import List
import logging
from minibus_routes import MinibusRoutes
from minibus_routes import RouteID

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class MinibusTracker(object):

    def __init__(self, debug=False):
        self.minibus_generator = MinibusGenerator(debug=debug)

        tracked_routes = [RouteID(route_number='246', type='b-a1')]

        self.routes = {route_id: route_data
                       for route_id, route_data in MinibusRoutes().items()
                       if route_id in tracked_routes}

        self.non_tracked_buses = None
        self.tracked_buses = {}

    def run(self):
        while True:
            current_time, self.non_tracked_buses = self.minibus_generator.get_minibuses()
            logger.debug('current_time = {}'.format(current_time))
            for route_id, route_data in self.routes.items():
                for car_id, minibus in self.non_tracked_buses.items():
                    try:
                        self.tracked_buses[car_id].location = minibus.location
                    except KeyError:
                        if (minibus.route_number == route_id.route_number and
                                self.is_bus_at_first_stop_in_route(minibus, route_data.stops)):
                            self.tracked_buses[car_id] = minibus

            for route_id, route_data in self.routes.items():
                for car_id, minibus in self.tracked_buses.copy().items():
                    if (minibus.route_number == route_id.route_number and
                            self.is_bus_at_last_stop_in_route(minibus, route_data.stops)):
                        del self.tracked_buses[car_id]

            logging.debug('tracked buses = {}'.format(len(self.tracked_buses)))

    def is_bus_at_first_stop_in_route(self, minibus, stops: List[MinibusStop]):
        return self.is_bus_at_terminus(minibus=minibus, stops=stops, start_station=True)

    def is_bus_at_last_stop_in_route(self, minibus, stops: List[MinibusStop]):
        return self.is_bus_at_terminus(minibus=minibus, stops=stops, start_station=False)

    @staticmethod
    def is_bus_at_terminus(minibus, stops: List[MinibusStop], start_station):
        return minibus.location - stops[0 if start_station else -1].location < 40


def main():
    minibus_tracker = MinibusTracker(debug=True)

    minibus_tracker.run()


if __name__ == '__main__':
    main()
