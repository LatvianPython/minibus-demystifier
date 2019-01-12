from minibus_routes import MinibusRoutes
from minibus_routes import RouteID
import hashlib
import itertools
from typing import NamedTuple


class TimetableIndex(NamedTuple):
    departure: int
    stop: int


def running_sum(integers):
    total = 0
    for integer in integers:
        total += int(integer)
        yield total


def decode_data(encoded_data, days):
    remaining_days = days - sum(int(days_active) for days_active in encoded_data[1::2])

    decoded_data = itertools.chain.from_iterable(
        [data] * int(for_days)
        for data, for_days in itertools.zip_longest(*[iter(encoded_data)] * 2, fillvalue=remaining_days)
    )
    return list(decoded_data)


def split_data(data, depth=4):
    if depth != 0:
        end_of_segment = data.index('')
        return [data[:end_of_segment]] + split_data(data[end_of_segment + 1:], depth - 1)
    return [data]


def explode_times(encoded_data):
    data = split_data(encoded_data.split(','))

    timetable = list(running_sum(data[0]))

    number_of_departures = len(timetable)

    valid_from, valid_to, weekdays = (decode_data(data_slice, number_of_departures) for data_slice in data[1:4])

    time_between_stops = [int(val.zfill(1)) for val in data[4]]

    delta_time = 5
    left_to_parse = number_of_departures
    for time_delta, stop_with_current_delta in itertools.zip_longest(*[iter(time_between_stops[:-2])] * 2, fillvalue=0):

        delta_time = delta_time + time_delta - 5

        if stop_with_current_delta > 0:
            left_to_parse = left_to_parse - stop_with_current_delta
        else:
            stop_with_current_delta, left_to_parse = left_to_parse, 0

        index_to = -(number_of_departures - stop_with_current_delta)

        if index_to == 0:
            index_to = None

        timetable += [departure_time + delta_time
                      for departure_time in timetable[-number_of_departures:index_to]]

        if left_to_parse <= 0:
            left_to_parse, delta_time = number_of_departures, 5

    return number_of_departures, {'weekdays': weekdays,
                                  'timetable': timetable,
                                  'valid_from': valid_from,
                                  'valid_to': valid_to}


class Timetable:

    def __init__(self, timetable: str):
        self.departures, timetable = explode_times(timetable)
        self.timetable = timetable['timetable']

    def __getitem__(self, pos):
        departure, stop = pos
        timetable_index = departure - 1 + stop * self.departures
        return self.timetable[timetable_index]


def main():
    routes = MinibusRoutes()

    desired_route = RouteID(route_number='246', type='a-b')

    route = routes[desired_route]

    timetable = Timetable(route.timetable)

    time_at_stop = timetable[TimetableIndex(departure=13, stop=0)]

    assert time_at_stop == 375

    hash_object = hashlib.md5(str(timetable.timetable).encode('utf-8'))
    digest = hash_object.hexdigest()
    test_digest = 'f88d7270866077f81c85a29131100292'

    assert digest == test_digest, 'hashes do not match anymore: {} != {}'.format(digest, test_digest)

    encoded_data_test = ['17728', '12', '17726']
    days_test = 79

    decoded_data = decode_data(encoded_data_test, days_test)
    assert len(decoded_data) == days_test
    assert decoded_data == ['17728', '17728', '17728', '17728', '17728', '17728', '17728', '17728', '17728', '17728',
                            '17728', '17728', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726',
                            '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726',
                            '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726',
                            '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726',
                            '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726',
                            '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726',
                            '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726', '17726']

    print('all ok')


if __name__ == '__main__':
    main()
