from geolocation import Geolocation
from minibus_generator import Minibus
from minibus_stops import MinibusStop
from slack_app import App
from nose.tools import assert_is_not_none


def test_slack_attachments():
    app = App()
    minibuses = [Minibus(route_number='224', speed=45, departure=35, heading=4, stop_index=3,
                         stop=MinibusStop(location=Geolocation(latitude=56.945, longitude=24.195),
                                          name='Progresa iela'),
                         location=Geolocation(latitude=56.946, longitude=24.196)),
                 Minibus(route_number='224', speed=45, departure=35, heading=4, stop_index=7,
                         stop=MinibusStop(location=Geolocation(latitude=56.945, longitude=24.195), name='Airītes iela'),
                         location=Geolocation(latitude=56.946, longitude=24.196)),
                 Minibus(route_number='224', speed=45, departure=35, heading=4, stop_index=0,
                         stop=MinibusStop(location=Geolocation(latitude=56.9, longitude=24.1), name='Dubultu iela'),
                         location=Geolocation(latitude=56.946, longitude=24.196))
                 ]

    attachments = app.format_for_slack(minibuses=minibuses)

    assert_is_not_none(attachments)
