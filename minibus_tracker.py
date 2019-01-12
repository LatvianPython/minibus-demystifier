from minibuses import Minibuses
from minibus_stops import MinibusStop
from minibus_routes import MinibusRoutes
from minibus_routes import RouteID


class MinibusTracker(object):

    def __init__(self):
        self.minibuses = Minibuses()

        tracked_routes = [RouteID(route_number='246', type='b-a1')]

        self.routes = {route_id: route_data
                       for route_id, route_data in MinibusRoutes().items()
                       if route_id in tracked_routes}

        # print(self.routes)

        self.non_tracked_buses = list(self.minibuses)

        self.tracked_buses = []

        for route_id, route_data in self.routes.items():
            for minibus in self.non_tracked_buses:
                if minibus.route_number == route_id.route_number:
                    if self.is_bus_at_terminal_station(minibus, route_data.stops[0]):
                        self.tracked_buses.append(minibus)
                        print(minibus.route_number, minibus.car_id, route_data.name)

    def is_bus_at_terminal_station(self, minibus, terminus: MinibusStop):
        return minibus.location - terminus.location < 40


def main():
    minibus_tracker = MinibusTracker()

    # for minibus in minibus_tracker.non_tracked_buses:
    #     print(minibus)


if __name__ == '__main__':
    main()
