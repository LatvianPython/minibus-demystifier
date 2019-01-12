import math
from typing import NamedTuple


def measure(lon1, lat1, lon2, lat2):
    r = 6378.137
    d_lat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    d_lon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + \
        math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(d_lon / 2) * math.sin(d_lon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = r * c
    return d * 1000


def distance_between_points(p1, p2):
    return measure(p1[0], p1[1], p2[0], p2[1])


class Geolocation(NamedTuple):
    longitude: float
    latitude: float

    def __sub__(self, other):
        return distance_between_points(self, other)


def main():
    distance = Geolocation(1.006, 1) - Geolocation(1, 1)
    assert int(distance) == 667


if __name__ == '__main__':
    main()
