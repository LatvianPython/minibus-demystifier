from minibus_tracker import MinibusTracker
import slackclient
from time import sleep
import configparser


def main():
    tracker = MinibusTracker()

    config_parser = configparser.ConfigParser()
    config_parser.read('config.ini')
    slack_token = config_parser['slack']['token']
    user = config_parser['slack']['user']
    stop = int(config_parser['slack']['stop'])

    slack = slackclient.SlackClient(slack_token)

    # for _ in range(275):
    #     tracker.refresh_minibuses()

    if slack.rtm_connect():
        while slack.server.connected is True:

            tracker.refresh_minibuses()

            minibuses = [minibus
                         for minibus in tracker.tracked_minibuses.values()
                         if minibus.stop_index <= stop]

            print(len(minibuses))
            if len(minibuses) > 0 or True:
                timetable = list(tracker.routes.values())[0].timetable


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
