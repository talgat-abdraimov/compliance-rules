"""Fixtures for soc2-logging.python.no-model-dump-in-logs. All data invented."""

import json
from dataclasses import asdict

from loguru import logger


def handle_webhook(payload, user):
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

    # pydantic v1 .dict(), stdlib vars()/asdict()/__dict__ and json.dumps of a variable.
    # ruleid: soc2-logging.python.no-model-dump-in-logs
    logger.info('legacy event', attrs=payload.dict())

    # ruleid: soc2-logging.python.no-model-dump-in-logs
    logger.info(f'legacy event: {payload.dict()}')

    # ruleid: soc2-logging.python.no-model-dump-in-logs
    logger.info('user snapshot', attrs=vars(user))

    # ruleid: soc2-logging.python.no-model-dump-in-logs
    logger.info('user snapshot', attrs=user.__dict__)

    # ruleid: soc2-logging.python.no-model-dump-in-logs
    logger.info('user snapshot', attrs=asdict(user))

    # ruleid: soc2-logging.python.no-model-dump-in-logs
    logger.info('user snapshot', attrs=user.to_dict())

    # ruleid: soc2-logging.python.no-model-dump-in-logs
    logger.info(f'serialized: {json.dumps(payload)}')

    # ok: soc2-logging.python.no-model-dump-in-logs
    logger.info('webhook event started', user_id=payload.user_id)

    # An inline literal dict names its own fields — nothing is dumped wholesale.
    # ok: soc2-logging.python.no-model-dump-in-logs
    logger.info('audit', attrs=json.dumps({'user_id': payload.user_id}))

    # ok: soc2-logging.python.no-model-dump-in-logs
    normalized = payload.model_dump()
    return normalized
