from typing import NamedTuple
from geolocation.calculations import distance_between_points


class Geolocation(NamedTuple):
    latitude: float
    longitude: float

    def __sub__(self, other):
        return distance_between_points(*self, *other)
