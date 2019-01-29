import requests
import logging
from io import StringIO
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def handle_response(response):
    if response.status_code == 200:
        logger.debug('response status: {}, length: {}, elapsed: {}, url: {}'.format(
            response.status_code,
            len(response.content),
            response.elapsed,
            response.url
        ))
    else:
        logger.critical(
            'request failed with {}, content = "{}", headers = "{}", cookies = "{}"'.format(
                response.status_code,
                response.content,
                response.headers,
                response.cookies)
        )
        response.raise_for_status()


def handle_request(url):
    with requests.get(url) as response:
        handle_response(response)
        content = response.content.decode('utf-8-sig')
        return StringIO(content)


def to_datetime(timestamp):
    try:
        return datetime.fromtimestamp(timestamp, timezone(timedelta(hours=2)))
    except TypeError:
        return to_datetime(int(timestamp))
