from minibus_routes import MinibusRoutes
from minibus_routes import RouteID
import hashlib


def running_sum(integers):
    total = 0
    for integer in integers:
        total += int(integer)
        yield total


def parse_days(encoded_data, days):
    # print(encoded_data)

    chunks = [encoded_data[x:x + 2] for x in range(0, len(encoded_data), 2)]
    # print(chunks)
    valid_from = []
    for day in chunks:
        try:
            valid_from += [day[0]] * int(day[1])
        except IndexError:
            valid_from += [day[0]] * (days - len(valid_from))

    # print('{} -> {}'.format(encoded_data, valid_from))
    return valid_from


def split_data(data, depth=4):
    if depth != 0:
        index = data.index('')
        return [data[:index]] + split_data(data[index + 1:], depth - 1)
    return [data]


def explode_times(encoded_data):
    # decoding times
    data = encoded_data.split(',')

    data = split_data(data)

    number_of_departures = len(data[0])

    timetable = list(running_sum(data[0]))

    valid_from = parse_days(data[1], number_of_departures)
    valid_to = parse_days(data[2], number_of_departures)
    weekdays = parse_days(data[3], number_of_departures)

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
    print('all ok')


if __name__ == '__main__':
    main()
