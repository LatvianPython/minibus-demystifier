from minibus_routes import MinibusRoutes
from minibus_routes import RouteID
import hashlib
import itertools


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

    number_of_departures = len(data[0])

    valid_from, valid_to, weekdays = (decode_data(data_slice, number_of_departures) for data_slice in data[1:4])

    time_between_stops = data[4]

    delta_time = 5
    left_to_parse = number_of_departures
    for i in range(0, len(time_between_stops) - 2, 2):
        times = (time_between_stops[i], time_between_stops[i + 1])
        delta_time = delta_time + int(time_between_stops[i]) - 5
        stop_with_current_delta = int(times[1].zfill(1))

        if stop_with_current_delta > 0:
            left_to_parse = left_to_parse - stop_with_current_delta
        else:
            stop_with_current_delta = left_to_parse
            left_to_parse = 0

        index_to = -(number_of_departures - stop_with_current_delta)
        if index_to == 0:
            index_to = None

        timetable += [departure_time + delta_time
                      for departure_time in timetable[-number_of_departures:index_to]]

        if left_to_parse <= 0:
            left_to_parse = number_of_departures
            delta_time = 5

    return {'weekdays': weekdays,
            'timetable': timetable,
            'valid_from': valid_from,
            'valid_to': valid_to}


def main():
    routes = MinibusRoutes()

    desired_route = RouteID(route_number='246', type='a-b')

    route = routes[desired_route]

    exploded_times = explode_times(route.timetable)

    hash_object = hashlib.md5(str(exploded_times).encode('utf-8'))
    digest = hash_object.hexdigest()
    test_digest = '11f0804c5eb09f80e0e77a3d62277cb9'

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
