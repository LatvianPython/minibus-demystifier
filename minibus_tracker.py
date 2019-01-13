from minibuses import Minibuses
from minibus_stops import MinibusStop
from typing import List
from minibus_routes import MinibusRoutes
from minibus_routes import RouteID


class MinibusTracker(object):

    def __init__(self, debug=False):
        self.minibuses = Minibuses(debug=debug)

        tracked_routes = [RouteID(route_number='246', type='b-a1')]

        self.routes = {route_id: route_data
                       for route_id, route_data in MinibusRoutes().items()
                       if route_id in tracked_routes}

        self.non_tracked_buses = None
        self.tracked_buses = {}

    def run(self):
        while True:
            self.non_tracked_buses = iter(self.minibuses)
            for route_id, route_data in self.routes.items():
                for minibus in self.non_tracked_buses:
                    if minibus.route_number == route_id.route_number:
                        if self.is_bus_at_terminal_station(minibus, route_data.stops):
                            print(minibus.car_id, 'at terminal station')

    @staticmethod
    def is_bus_at_terminal_station(minibus, stops: List[MinibusStop]):
        return minibus.location - stops[0].location < 40

    @staticmethod
    def closest_stop(minibus, stops: List[MinibusStop]):
        return min([(stop, minibus.location - stop.location)
                    for stop in stops],
                   key=lambda a: a[1])


def main():
    minibus_tracker = MinibusTracker(debug=True)

    minibus_tracker.run()


if __name__ == '__main__':
    main()
