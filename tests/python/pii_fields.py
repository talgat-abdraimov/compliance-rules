"""Fixtures for soc2-logging.python.no-pii-fields-in-logs. All data invented."""

from loguru import logger


def notify(user, email, message, user_id):
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

    # ok: soc2-logging.python.no-pii-fields-in-logs
    logger.info('notification sent', email_id=message.email_id, user_id=user_id)

    # ok: soc2-logging.python.no-pii-fields-in-logs
    logger.info('detection event', sender_id=message.sender_id)

    # ok: soc2-logging.python.no-pii-fields-in-logs
    send_email(email)

    # R5 verification: suppression must hold WITH trailing justification text.
    # nosemgrep: soc2-logging.python.no-pii-fields-in-logs — sanitized upstream, see contracts/rule-conventions.md
    logger.info('suppression probe', email=email)

    return log


def send_email(email):
    """Not a logging sink — the denylist must not fire outside log calls."""
    return email
