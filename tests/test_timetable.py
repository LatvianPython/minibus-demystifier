import hashlib
from minibus_routes import MinibusRoutes
from minibus_routes import RouteID
from timetable import TimetableIndex
from timetable import Timetable
from timetable import decode_data
from nose.tools import assert_equal


def test_decoding():
    encoded_data_test = ['17728', '12', '17726']
    days_test = 79

    decoded_data = decode_data(encoded_data_test, days_test)
    assert_equal(len(decoded_data), days_test)

    correct_decode_data = ['17728', '17728', '17728', '17728', '17728', '17728', '17728', '17728', '17728', '17728',
                           '17728', '17728', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726',
                           '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726',
                           '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726',
                           '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726',
                           '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726',
                           '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726',
                           '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726']

    assert_equal(decoded_data, correct_decode_data)


def test_timetable():
    routes = MinibusRoutes()
    desired_route = RouteID(route_number='246', type='a-b')
    route = routes[desired_route]

    timetable = Timetable(route.timetable)

    time_at_stop = timetable[TimetableIndex(departure=13, stop=0)]

    hash_object = hashlib.md5(str(timetable.timetable).encode('utf-8'))
    digest = hash_object.hexdigest()
    expected_digest = 'f88d7270866077f81c85a29131100292'

    assert_equal(time_at_stop, 375)
    assert_equal(digest, expected_digest)
