from minibus_generator import MinibusGenerator
from datetime import datetime
from nose.tools import assert_equal
from nose.tools import assert_greater


def get_minibus_data(minibuses):
    timestamp, minibus_generator = minibuses.get_minibuses()
    return timestamp, list(minibus_generator)


def test_minibuses():
    minibus_generator = MinibusGenerator(debug=True)

    timestamp, current_minibuses = get_minibus_data(minibus_generator)
    should_be = datetime(2018, 9, 12, 16, 37, 51)

    assert_equal(timestamp, should_be)
    assert_equal(len(current_minibuses), 149)

    timestamp, _ = get_minibus_data(minibus_generator)

    assert_greater(timestamp, should_be)


def test_integration():
    minibus_generator = MinibusGenerator()

    _, current_minibuses = get_minibus_data(minibus_generator)

    assert_greater(len(current_minibuses), 0)
