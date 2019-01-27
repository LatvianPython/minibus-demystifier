from minibus_routes import RouteID
from minibus_tracker import MinibusTracker
from nose.tools import assert_greater


def test_refresh():
    minibus_tracker = MinibusTracker(RouteID(route_number='246', type='a1-b'), debug=True)

    for i in range(250):
        minibus_tracker.refresh_minibuses()

    assert_greater(len(minibus_tracker.tracked_minibuses), 0)
