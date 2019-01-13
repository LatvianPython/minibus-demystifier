from geolocation import Geolocation
from minibus_stops import closest_stop
from minibus_routes import MinibusRoutes, RouteID
from minibus_generator import Minibus
from nose.tools import assert_equal


def test_closest():
    stops = MinibusRoutes()[RouteID(route_number='246', type='a1-b')].stops

    minibus = Minibus(route_number='246', location=Geolocation(latitude=56.965532, longitude=24.167770),
                      speed=0, heading=0)

    index, stop = closest_stop(minibus=minibus, stops=stops)

    assert_equal(index, 11)
