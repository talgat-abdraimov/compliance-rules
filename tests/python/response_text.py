"""Fixtures for soc2-logging.python.no-response-text-in-logs. All data invented."""

from loguru import logger


def call_maps_api(client, response):
    # ruleid: soc2-logging.python.no-response-text-in-logs
    logger.error(f'google api error body: {response.text}')

    # ruleid: soc2-logging.python.no-response-text-in-logs
    logger.error('upstream failed', body=response.content)

    resp = client.get('/geocode')
    # ruleid: soc2-logging.python.no-response-text-in-logs
    logger.warning(f'unexpected payload: {resp.text}')

    logger.error(
        'upstream failed',
        # ruleid: soc2-logging.python.no-response-text-in-logs
        raw=response.text,
    )

    # ok: soc2-logging.python.no-response-text-in-logs
    logger.error('google api error', status_code=response.status_code)

    # ok: soc2-logging.python.no-response-text-in-logs
    logger.info('response received', response_size=len(response.content))

    # ok: soc2-logging.python.no-response-text-in-logs
    logger.debug('body length', text_len=len(response.text))

    # ok: soc2-logging.python.no-response-text-in-logs
    parsed = response.text
    return parsed
