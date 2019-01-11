import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def handle_response(response):
    if response.status_code == 200:
        logger.debug('response status: {}, length: {}'.format(response.status_code, len(response.content)))
    else:
        logger.critical(
            'request failed with {}, content = "{}", headers = "{}", cookies = "{}"'.format(
                response.status_code,
                response.content,
                response.headers,
                response.cookies)
        )
        response.raise_for_status()
