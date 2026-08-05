"""Fixtures for soc2-logging.python.no-tokens-in-logs. All tokens invented."""

from loguru import logger


def manage_session(session, access_token, api_key, user_id):
    # ruleid: soc2-logging.python.no-tokens-in-logs
    logger.info('item removed', access_token=access_token)

    # ruleid: soc2-logging.python.no-tokens-in-logs
    logger.info(f'created new session: {session.session_token}')

    # ruleid: soc2-logging.python.no-tokens-in-logs
    logger.debug('calling upstream', api_key=api_key)

    # ruleid: soc2-logging.python.no-tokens-in-logs
    logger.warning('auth failed', authorization=session.authorization)

    token_str = str(session.session_token)
    # ruleid: soc2-logging.python.no-tokens-in-logs
    logger.warning(f'session already completed: {token_str}')

    # ruleid: soc2-logging.python.no-tokens-in-logs
    logger.info(
        'session reused',
        session_token=session.session_token,
        user_id=user_id,
    )

    # ok: soc2-logging.python.no-tokens-in-logs
    logger.info('item removed', user_id=user_id)

    # ok: soc2-logging.python.no-tokens-in-logs
    logger.info('session validated', token_id=session.token_id)

    # ok: soc2-logging.python.no-tokens-in-logs
    logger.debug('auth state', has_token=bool(access_token))
