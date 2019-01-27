import itertools
import logging
from typing import NamedTuple

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


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
    @staticmethod
    def format_time(minutes):
        """ returns string representation of a timetable record
        """
        return '{}:{}'.format(str(int(minutes / 60) % 24).rjust(2), str(minutes % 60).zfill(2))

    def __init__(self, timetable: str):
        self.departures, timetable = explode_times(timetable)
        self.timetable = timetable['timetable']

    def __getitem__(self, pos: TimetableIndex):
        departure, stop = pos.departure, pos.stop
        timetable_index = departure + stop * self.departures
        time_value = self.timetable[timetable_index]
        logging.debug('{} {}'.format(timetable_index, time_value))
        return time_value

    def closest_departure(self, current_time, closest_stop_index):
        time_value = current_time.minute + current_time.hour * 60
        logging.debug('time_value = {}'.format(time_value))
        departure, _ = min(((i, abs(self[TimetableIndex(departure=i, stop=closest_stop_index)] - time_value))
                            for i in range(self.departures)),
                           key=lambda a: a[1])
        return departure

    # todo: change to also take into account location of minibus to allow for second precision?
    def time_to_stop(self, departure, current_stop, target_stop):
        return abs(self[TimetableIndex(departure=departure, stop=current_stop)] -
                   self[TimetableIndex(departure=departure, stop=target_stop)])
