"""Fixtures for soc2-logging.python.no-model-dump-in-logs. All data invented."""

from loguru import logger


def handle_webhook(payload):
    # ruleid: soc2-logging.python.no-model-dump-in-logs
    logger.info('webhook event started', payload=payload.model_dump())

    # ruleid: soc2-logging.python.no-model-dump-in-logs
    logger.error('unknown offer', data=payload.model_dump_json())

    # ruleid: soc2-logging.python.no-model-dump-in-logs
    logger.info(f'raw event: {payload.model_dump()}')

    # ruleid: soc2-logging.python.no-model-dump-in-logs
    logger.warning('fallback event', attrs=dict(payload))

    logger.info(
        'payments oneclick finished',
        # ruleid: soc2-logging.python.no-model-dump-in-logs
        payload=payload.model_dump(),
    )

    # ok: soc2-logging.python.no-model-dump-in-logs
    logger.info('webhook event started', user_id=payload.user_id)

    # ok: soc2-logging.python.no-model-dump-in-logs
    normalized = payload.model_dump()
    return normalized
