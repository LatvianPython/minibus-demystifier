from minibus_generator import MinibusGenerator
from minibus_stops import closest_stop
import logging
from minibus_routes import MinibusRoutes
from minibus_routes import RouteID

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class MinibusTracker(object):

    def __init__(self, tracked_route, debug=False):
        self.minibus_generator = MinibusGenerator(debug=debug)

        self.route_id, self.route_data = tracked_route, MinibusRoutes()[tracked_route]

        self.tracked_minibuses = {}

    def refresh_minibuses(self):
        current_time, non_tracked_buses = self.minibus_generator.get_minibuses()
        logger.debug('current_time = {}'.format(current_time))

        non_tracked_buses = {car_id: minibus
                             for car_id, minibus in non_tracked_buses.items()
                             if minibus.route_number == self.route_id.route_number
                             }

        for car_id, minibus in non_tracked_buses.items():
            if car_id in self.tracked_minibuses or self.at_first_stop(minibus=minibus):
                # fixme: these could probably just be calculated when needed...?
                minibus.stop_index, minibus.stop = closest_stop(minibus=minibus, stops=self.route_data.stops)

                minibus.departure = self.route_data.timetable.closest_departure(current_time=current_time,
                                                                                closest_stop_index=minibus.stop_index)
                minibus.times_not_found = 0
                self.tracked_minibuses[car_id] = minibus

        # minibuses sometimes can not appear in gps data intermittently for a few reading, make sure not to lose them
        for car_id in self.tracked_minibuses.keys():
            if car_id not in non_tracked_buses.keys():
                self.tracked_minibuses[car_id].times_not_found += 1

        self.tracked_minibuses = {car_id: minibus
                                  for car_id, minibus in self.tracked_minibuses.items()
                                  if minibus.times_not_found < 5
                                  if not self.at_last_stop(minibus=minibus)
                                  }

    def at_first_stop(self, minibus):
        return closest_stop(minibus=minibus, stops=self.route_data.stops).stop_index == 0

    def at_last_stop(self, minibus):
        return closest_stop(minibus=minibus, stops=self.route_data.stops).stop_index == (len(self.route_data.stops) - 1)


def main():
    minibus_tracker = MinibusTracker(RouteID(route_number='246', type='a1-b'), debug=True)

    for i in range(1875):
        minibus_tracker.refresh_minibuses()

        print(i, len(minibus_tracker.tracked_minibuses))


if __name__ == '__main__':
    main()
