from time import sleep
from minibus_routes import RouteID
from minibus_tracker import MinibusTracker


def main():
    tracked_route = RouteID(route_number='204', type='a-b')
    tracker = MinibusTracker(tracked_route=tracked_route)
    while True:
        tracker.refresh_minibuses()

        # just a basic example, possible to also use route timetable from the tracker
        # to determine time between stop and minibus
        for car_id, minibus in tracker.tracked_minibuses.items():
            print(minibus.stop.name, minibus.location)

        sleep(5)


if __name__ == '__main__':
    main()
