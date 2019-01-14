from minibus_generator import MinibusGenerator
from minibus_stops import MinibusStop, closest_stop
from typing import List
import logging
from minibus_routes import MinibusRoutes
from minibus_routes import RouteID

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class MinibusTracker(object):

    def __init__(self, tracked_route, debug=False):
        self.minibus_generator = MinibusGenerator(debug=debug)

        self.route_id, self.route_data = tracked_route, MinibusRoutes()[tracked_route]

        self.non_tracked_buses = None
        self.tracked_minibuses = {}

    def refresh_minibuses(self):
        current_time, self.non_tracked_buses = self.minibus_generator.get_minibuses()
        logger.debug('current_time = {}'.format(current_time))

        for car_id, minibus in self.non_tracked_buses.items():
            if (car_id in self.tracked_minibuses or (
                    minibus.route_number == self.route_id.route_number and
                    closest_stop(minibus=minibus, stops=self.route_data.stops)[0] == 0)):
                minibus.stop_index, minibus.stop = closest_stop(minibus=minibus, stops=self.route_data.stops)
                minibus.departure = self.route_data.timetable.closest_departure(
                    current_time=current_time,
                    closest_stop_index=minibus.stop_index
                )
                minibus.times_not_found = 0
                self.tracked_minibuses[car_id] = minibus

        for car_id, minibus in self.tracked_minibuses.copy().items():
            if (minibus.route_number == self.route_id.route_number and
                    closest_stop(minibus=minibus, stops=self.route_data.stops)[0] == (len(self.route_data.stops) - 1)):
                del self.tracked_minibuses[car_id]

        for car_id in self.tracked_minibuses.keys():
            if car_id not in self.non_tracked_buses.keys():
                self.tracked_minibuses[car_id].times_not_found += 1

        self.tracked_minibuses = {car_id: minibus
                                  for car_id, minibus in self.tracked_minibuses.items()
                                  if minibus.times_not_found < 5
                                  }

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
    minibus_tracker = MinibusTracker(RouteID(route_number='246', type='a1-b'), debug=True)

    # minibus_tracker.run()

    for i in range(1875):
        minibus_tracker.refresh_minibuses()

        print(i, len(minibus_tracker.tracked_minibuses))


if __name__ == '__main__':
    main()
