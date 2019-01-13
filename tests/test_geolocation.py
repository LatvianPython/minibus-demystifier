from nose.tools import assert_equals
from geolocation import Geolocation


def test_distance_calculations():
    distance = Geolocation(1.006, 1) - Geolocation(1, 1)
    assert_equals(int(distance), 667)
