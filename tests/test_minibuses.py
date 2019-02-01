from minibus_generator import MinibusGenerator
from utility import to_datetime
from nose.tools import assert_equal
from nose.tools import assert_greater


def get_minibus_data(minibuses):
    timestamp, minibus_generator = minibuses.get_minibuses('246')
    return timestamp, list(minibus_generator)


def test_minibuses():
    minibus_generator = MinibusGenerator(debug=True)

    timestamp, current_minibuses = get_minibus_data(minibus_generator)
    should_be = to_datetime(1536770271)

    assert_equal(timestamp, should_be, '{} != {}'.format(timestamp, should_be))
    assert_equal(len(current_minibuses), 6)

    timestamp, _ = get_minibus_data(minibus_generator)

    assert_greater(timestamp, should_be)
