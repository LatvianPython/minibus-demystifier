from minibus_routes import RouteID
from minibus_tracker import MinibusTracker


def test_refresh():
    minibus_tracker = MinibusTracker(RouteID(route_number='246', type='a1-b'), debug=True)

    for i in range(250):
        minibus_tracker.refresh_minibuses()
