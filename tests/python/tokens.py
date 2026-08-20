"""Fixtures for soc2-logging.python.no-tokens-in-logs. All tokens invented."""

from loguru import logger

LOGGER = logger


def manage_session(session, access_token, api_key, user_id, usage, num_tokens, max_tokens):
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

    # ruleid: soc2-logging.python.no-tokens-in-logs
    logger.info('calling upstream with %s', api_key)

    # ruleid: soc2-logging.python.no-tokens-in-logs
    LOGGER.info('item removed', client_secret=session.client_secret)

    # ruleid: soc2-logging.python.no-tokens-in-logs
    logger.info('item removed', extra={'access_token': access_token})

    # ok: soc2-logging.python.no-tokens-in-logs
    logger.info('item removed', user_id=user_id)

    # ok: soc2-logging.python.no-tokens-in-logs
    logger.info('session validated', token_id=session.token_id)

    # ok: soc2-logging.python.no-tokens-in-logs
    logger.debug('auth state', has_token=bool(access_token))

    # LLM token counts are metrics, not credentials.
    # ok: soc2-logging.python.no-tokens-in-logs
    logger.info('llm call finished', prompt_tokens=usage.prompt_tokens, max_tokens=512)

    # ok: soc2-logging.python.no-tokens-in-logs
    logger.info(f'used {num_tokens} of {max_tokens} tokens')

    # ok: soc2-logging.python.no-tokens-in-logs
    logger.info('budget', token_count=usage.token_count, tokens_used=usage.tokens_used)

    # A quoted constant naming a credential kind is not a credential.
    # ok: soc2-logging.python.no-tokens-in-logs
    logger.info('token grant', grant_type='password')

    # Secret references are not secret values.
    # ok: soc2-logging.python.no-tokens-in-logs
    logger.info('fetching credentials', secret_name='prod/plaid', token_url=session.token_url)
