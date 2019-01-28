from minibus_routes import RouteID
from minibus_tracker import MinibusTracker
import slackclient
from time import sleep
import configparser


class App:
    def create_attachment(self, minibus):
        time_to_stop = self.timetable.time_to_stop(departure=minibus.departure,
                                                   current_stop=minibus.stop_index,
                                                   target_stop=self.stop_index)

        color_dict = {'danger': range(0, 9),
                      'warning': range(10, 14),
                      'good': range(15, 120)}

        color = next((color
                      for color, time_range in color_dict.items()
                      if time_to_stop in time_range), 'good')

        attachment = {
            'fallback': 'Minibus in {} minutes'.format(time_to_stop),
            'color': color,
            'title': 'Minibus currently near {}'.format(minibus.stop.name),
            'fields': [{'title': 'Stops to go:',
                        'value': self.stop_index - minibus.stop_index,
                        'short': True},
                       {'title': 'Arrives in:',
                        'value': '{} minutes'.format(time_to_stop),
                        'short': True}]
        }

        return attachment, time_to_stop

    def format_for_slack(self, minibuses):

        attachments = [self.create_attachment(minibus) for minibus in minibuses]

        attachments = [attachment for attachment, _ in sorted(attachments, key=lambda a: a[1], reverse=True)]

        return attachments

    def get_last_bot_comment(self):
        response = self.slack.api_call('im.history', channel=self.channel, count=10)
        try:
            min_timestamp = max(message['ts'] for message in response['messages']
                                if 'bot_id' in message)
            return min_timestamp
        except ValueError:
            return None

    def update_message(self, attachments):
        self.timestamp = self.get_last_bot_comment()
        if self.timestamp is not None:
            return self.slack.api_call('chat.update', channel=self.channel, ts=self.timestamp,
                                       attachments=attachments, as_user=False)
        return None

    def delete_latest_bot_message(self):
        self.timestamp = self.get_last_bot_comment()
        if self.timestamp is not None:
            return self.slack.api_call('chat.delete', channel=self.channel, ts=self.timestamp, as_user=True)
        return None

    def post_message(self, attachments):
        return self.slack.api_call('chat.postMessage', channel=self.channel, attachments=attachments)

    def __init__(self):
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini')

        slack_config = config_parser['slack']

        slack_token = slack_config['token']
        self.channel = slack_config['channel']
        self.stop_index = int(slack_config['stop'])

        self.slack = slackclient.SlackClient(slack_token)

        self.timestamp = self.get_last_bot_comment()

        route_config = config_parser['tracked_route']

        tracked_route = RouteID(route_number=route_config['route_number'], type=route_config['type'])
        self.tracker = MinibusTracker(tracked_route=tracked_route)

        self.stop = self.tracker.route_data.stops[self.stop_index]

        self.timetable = self.tracker.route_data.timetable

        self.last_message = None

        self.no_nearby_message = [{
            'fallback': 'No minibuses incoming',
            'color': '#E3E4E6',  # grey
            'title': 'No minibuses incoming'
        }]

        if not self.slack.rtm_connect():
            raise RuntimeError('Could not connect to Slack RTM')

    def refresh_slack(self):
        self.tracker.refresh_minibuses()

        minibuses = [minibus
                     for minibus in self.tracker.tracked_minibuses.values()
                     if minibus.stop_index <= self.stop_index]

        if len(minibuses) > 0:
            attachments = self.format_for_slack(minibuses=minibuses)
        else:
            attachments = self.no_nearby_message

        if attachments != self.last_message:
            self.delete_latest_bot_message()
            self.post_message(attachments=attachments)
            self.last_message = attachments

    def run(self):
        while self.slack.server.connected is True:
            self.refresh_slack()
            sleep(5)


def main():
    app = App()
    app.run()


if __name__ == '__main__':
    main()
