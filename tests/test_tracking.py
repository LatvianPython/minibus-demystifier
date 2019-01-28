from minibus_routes import RouteID
from minibus_tracker import MinibusTracker
from nose.tools import assert_equal


def test_refresh():
    minibus_tracker = MinibusTracker(RouteID(route_number='246', type='a1-b'), debug=True)

    for i in range(250):
        minibus_tracker.refresh_minibuses()

    assert_equal(len(minibus_tracker.tracked_minibuses), 1)

    minibus = minibus_tracker.tracked_minibuses.popitem()[1]

    assert_equal('Katlakalna iela', minibus.stop.name)
