from minibus_routes import RouteID
from minibus_tracker import MinibusTracker
import slackclient
from time import sleep
import configparser


def main():
    config_parser = configparser.ConfigParser()
    config_parser.read('config.ini')

    slack_config = config_parser['slack']

    slack_token = slack_config['token']
    user = slack_config['user']
    stop = int(slack_config['stop'])

    route_config = config_parser['tracked_route']

    tracked_route = RouteID(route_number=route_config['route_number'], type=route_config['type'])
    tracker = MinibusTracker(tracked_route=tracked_route)

    slack = slackclient.SlackClient(slack_token)

    if slack.rtm_connect():
        while slack.server.connected is True:

            tracker.refresh_minibuses()

            minibuses = [minibus
                         for minibus in tracker.tracked_minibuses.values()
                         if minibus.stop_index <= stop]

            print(len(minibuses))
            if len(minibuses) > 0 or True:
                timetable = tracker.route_data.timetable

                msg = ''
                for minibus in minibuses:
                    time_to_stop = timetable.time_to_stop(departure=minibus.departure,
                                                          current_stop=minibus.stop_index,
                                                          target_stop=stop)

                    msg += 'minibus will arrive in {} minutes\n'.format(time_to_stop)

                slack.api_call('chat.postMessage', channel=user, text=msg)
            sleep(5)
    else:
        print('Connection Failed')


if __name__ == '__main__':
    main()
