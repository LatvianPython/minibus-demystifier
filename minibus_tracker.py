from minibus_generator import MinibusGenerator
from minibus_stops import MinibusStop, closest_stop
from typing import List
import logging
from minibus_routes import MinibusRoutes
from minibus_routes import RouteID

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class MinibusTracker(object):

    def __init__(self, debug=False):
        self.minibus_generator = MinibusGenerator(debug=debug)

        tracked_routes = [RouteID(route_number='246', type='a1-b')]

        self.routes = {route_id: route_data
                       for route_id, route_data in MinibusRoutes().items()
                       if route_id in tracked_routes}

        self.non_tracked_buses = None
        self.tracked_minibuses = {}

    def refresh_minibuses(self):
        current_time, self.non_tracked_buses = self.minibus_generator.get_minibuses()
        logger.debug('current_time = {}'.format(current_time))
        for route_id, route_data in self.routes.items():
            for car_id, minibus in self.non_tracked_buses.items():
                if (car_id in self.tracked_minibuses or (
                        minibus.route_number == route_id.route_number and
                        self.is_bus_at_first_stop_in_route(minibus, route_data.stops))):
                    minibus.closest_stop = closest_stop(minibus=minibus, stops=route_data.stops)
                    minibus.departure = route_data.timetable.closest_departure(
                        current_time=current_time,
                        closest_stop_index=minibus.closest_stop[0]
                    )
                    minibus.times_not_found = 0
                    self.tracked_minibuses[car_id] = minibus

        for route_id, route_data in self.routes.items():
            for car_id, minibus in self.tracked_minibuses.copy().items():
                if (minibus.route_number == route_id.route_number and
                        self.is_bus_at_last_stop_in_route(minibus, route_data.stops)):
                    del self.tracked_minibuses[car_id]

        for car_id, minibus in self.tracked_minibuses.items():
            if car_id in self.non_tracked_buses.keys():
                self.tracked_minibuses[car_id].times_not_found += 1

        self.tracked_minibuses = {car_id: minibus
                                  for car_id, minibus in self.tracked_minibuses.items()
                                  if car_id in self.non_tracked_buses.keys() and
                                  minibus.times_not_found < 10
                                  }

        for car_id, minibus in self.tracked_minibuses.items():
            print(current_time, car_id, minibus.location, minibus.closest_stop[0], minibus.closest_stop[1].name,
                  minibus.departure, sep='\t')

    def run(self):
        while True:
            self.refresh_minibuses()
            logging.debug('tracked buses = {}'.format(len(self.tracked_minibuses)))

    def is_bus_at_first_stop_in_route(self, minibus, stops: List[MinibusStop]):
        return self.is_bus_at_terminus(minibus=minibus, stops=stops, start_station=True)

    def is_bus_at_last_stop_in_route(self, minibus, stops: List[MinibusStop]):
        return self.is_bus_at_terminus(minibus=minibus, stops=stops, start_station=False)

    @staticmethod
    def is_bus_at_terminus(minibus, stops: List[MinibusStop], start_station):
        return minibus.location - stops[0 if start_station else -1].location < 300


def main():
    minibus_tracker = MinibusTracker(debug=True)

    # minibus_tracker.run()

    for i in range(1875):
        minibus_tracker.refresh_minibuses()

        # print(i, len(minibus_tracker.tracked_minibuses))


if __name__ == '__main__':
    main()
