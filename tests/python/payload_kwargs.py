"""Fixtures for soc2-logging.python.no-full-payload-kwargs. All data invented."""

from loguru import logger


def consume(payload, data, event, kwargs, args, user_id):
    # ruleid: soc2-logging.python.no-full-payload-kwargs
    logger.info('vendor webhook received', payload=payload)

    # ruleid: soc2-logging.python.no-full-payload-kwargs
    logger.warning('item id not found', data=data)

    # ruleid: soc2-logging.python.no-full-payload-kwargs
    logger.info('cancellation requested', event=event)

    # ruleid: soc2-logging.python.no-full-payload-kwargs
    logger.error('client error', kwargs=kwargs)

    # ruleid: soc2-logging.python.no-full-payload-kwargs
    logger.error('client error', args=args)

    # ruleid: soc2-logging.python.no-full-payload-kwargs
    logger.info(
        'negotiation payment result',
        payload=payload,
        user_id=user_id,
    )

    # Positional args, f-strings and extra={...} bind the same whole object.
    # ruleid: soc2-logging.python.no-full-payload-kwargs
    logger.info('vendor webhook received', payload)

    # ruleid: soc2-logging.python.no-full-payload-kwargs
    logger.info(f'vendor webhook received: {payload}')

    # ruleid: soc2-logging.python.no-full-payload-kwargs
    logger.info('vendor webhook received', extra={'payload': payload})

    # ok: soc2-logging.python.no-full-payload-kwargs
    logger.info('vendor webhook received', webhook_code=payload.webhook_code)

    # ok: soc2-logging.python.no-full-payload-kwargs
    logger.info('cancellation requested', event_id=event.id, user_id=user_id)

    # ok: soc2-logging.python.no-full-payload-kwargs
    logger.info(f'vendor webhook received: {payload.webhook_code}')

    # ok: soc2-logging.python.no-full-payload-kwargs
    logger.info('vendor webhook received', payload_id=payload.id)

    # ok: soc2-logging.python.no-full-payload-kwargs
    logger.info('vendor webhook received', extra={'user_id': user_id})

    # ok: soc2-logging.python.no-full-payload-kwargs
    logger.info('vendor webhook received', source='data')


def exception_handler(exc, **kwargs):
    # ruleid: soc2-logging.python.no-full-payload-kwargs
    log_attrs = {'payload': kwargs.get('payload', {}), 'user_id': kwargs.get('user_id')}
    logger.exception('service error', **log_attrs)

    # ok: soc2-logging.python.no-full-payload-kwargs
    safe_attrs = {'user_id': kwargs.get('user_id'), 'error_type': type(exc).__name__}
    logger.exception('service error', **safe_attrs)
