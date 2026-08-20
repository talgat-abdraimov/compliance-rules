"""Fixtures for soc2-logging.python.no-pii-fields-in-logs. All data invented."""

from loguru import logger

LOGGER = logger
_logger = logger


def notify(user, email, message, user_id, phone_number, body):
    # ruleid: soc2-logging.python.no-pii-fields-in-logs
    logger.info('mail handler started', email=email, subject=message.subject)

    # ruleid: soc2-logging.python.no-pii-fields-in-logs
    logger.info(f'sending notification to {email}')

    # ruleid: soc2-logging.python.no-pii-fields-in-logs
    logger.warning('detection event', sender=message.sender, snippet=message.email_snippet)

    # ruleid: soc2-logging.python.no-pii-fields-in-logs
    logger.info('client info updated', client_ip=user.client_ip)

    # ruleid: soc2-logging.python.no-pii-fields-in-logs
    logger.debug('card check', card_number=user.card_number)

    # ruleid: soc2-logging.python.no-pii-fields-in-logs
    log = logger.bind(email=email)

    # ruleid: soc2-logging.python.no-pii-fields-in-logs
    logger.info(
        'subscription detected',
        service_name='StreamFlix',
        sender=message.sender,
    )

    # %-style and bare positional arguments are log arguments too.
    # ruleid: soc2-logging.python.no-pii-fields-in-logs
    logger.info('sending notification to %s', email)

    # ruleid: soc2-logging.python.no-pii-fields-in-logs
    logger.info(email)

    # ruleid: soc2-logging.python.no-pii-fields-in-logs
    logger.info('recipient resolved', arg=user.email)

    # Denylist terms carry suffixes: phone_number, address_line1, card_expiry.
    # ruleid: soc2-logging.python.no-pii-fields-in-logs
    logger.info('sms queued', phone_number=phone_number)

    # ruleid: soc2-logging.python.no-pii-fields-in-logs
    logger.info(f'sms queued for {phone_number}')

    # ruleid: soc2-logging.python.no-pii-fields-in-logs
    logger.info('shipping set', address_line1=user.address_line1)

    # ruleid: soc2-logging.python.no-pii-fields-in-logs
    logger.info('pickup set', latitude=user.latitude, longitude=user.longitude)

    # Identity documents are PII despite the _id suffix.
    # ruleid: soc2-logging.python.no-pii-fields-in-logs
    logger.info('kyc submitted', national_id=user.national_id)

    # Logger aliases: LOGGER, _logger, self._log.
    # ruleid: soc2-logging.python.no-pii-fields-in-logs
    LOGGER.info('mail handler started', email=email)

    # ruleid: soc2-logging.python.no-pii-fields-in-logs
    _logger.info('mail handler started', email=email)

    # stdlib logging extra={...} and any other dict inside a log call.
    # ruleid: soc2-logging.python.no-pii-fields-in-logs
    logger.info('mail handler started', extra={'email': email})

    # ruleid: soc2-logging.python.no-pii-fields-in-logs
    logger.info('mail handler started', extra={'recipient': email})

    # ok: soc2-logging.python.no-pii-fields-in-logs
    logger.info('notification sent', email_id=message.email_id, user_id=user_id)

    # ok: soc2-logging.python.no-pii-fields-in-logs
    logger.info('detection event', sender_id=message.sender_id)

    # ok: soc2-logging.python.no-pii-fields-in-logs
    logger.info('digest built', email_count=3, has_email=True, address_hash=user.address_hash)

    # ok: soc2-logging.python.no-pii-fields-in-logs
    logger.info(f'received {len(body)} bytes')

    # ok: soc2-logging.python.no-pii-fields-in-logs
    logger.info('upstream latency', p99_lat=42.0, avg_lat=11.5)

    # ok: soc2-logging.python.no-pii-fields-in-logs
    logger.info('mail handler started', extra={'user_id': user_id})

    # Quoted constants are literals, not the user's data.
    # ok: soc2-logging.python.no-pii-fields-in-logs
    logger.info('notification queued', channel='email', payment_method='card')

    # ok: soc2-logging.python.no-pii-fields-in-logs
    logger.info('notification queued', extra={'channel': 'email'})

    # ok: soc2-logging.python.no-pii-fields-in-logs
    send_email(email)

    # R5 verification: suppression must hold WITH trailing justification text.
    # nosemgrep: soc2-logging.python.no-pii-fields-in-logs — sanitized upstream, see contracts/rule-conventions.md
    logger.info('suppression probe', email=email)

    return log


def send_email(email):
    """Not a logging sink — the denylist must not fire outside log calls."""
    return email
