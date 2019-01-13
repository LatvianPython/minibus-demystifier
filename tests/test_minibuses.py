from minibuses import Minibuses
from datetime import datetime
from nose.tools import assert_equal
from nose.tools import assert_greater


def get_minibus_data(minibuses):
    timestamp, minibus_generator = minibuses.get_minibuses()
    timestamp = datetime.utcfromtimestamp(timestamp)
    return timestamp, list(minibus_generator)


def test_minibuses():
    minibuses = Minibuses(debug=True)

    timestamp, current_minibuses = get_minibus_data(minibuses)
    should_be = datetime(2018, 9, 12, 16, 37, 51)

    assert_equal(timestamp, should_be)
    assert_equal(len(current_minibuses), 149)

    timestamp, _ = get_minibus_data(minibuses)

    assert_greater(timestamp, should_be)


def test_integration():
    minibuses = Minibuses()

    _, current_minibuses = get_minibus_data(minibuses)

    assert_greater(len(current_minibuses), 0)
