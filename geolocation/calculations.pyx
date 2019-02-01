from libc.math cimport sin
from libc.math cimport pi
from libc.math cimport cos
from libc.math cimport atan2
from libc.math cimport sqrt


cpdef double distance_between_points(double lon1, double lat1, double lon2, double lat2):
    """Returns distance between two (lat,lng) pairs in meters"""
    cdef double d_lat, d_lon, a, c, d
    cdef double r = 6378.137
    d_lat = lat2 * pi / 180 - lat1 * pi / 180
    d_lon = lon2 * pi / 180 - lon1 * pi / 180
    a = (sin(d_lat / 2) * sin(d_lat / 2) +
         (cos(lat1 * pi / 180) * cos(lat2 * pi / 180) *
          sin(d_lon / 2) * sin(d_lon / 2)))
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = r * c
    return d * 1000
