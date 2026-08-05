# Logging compliance (SOC2)

> Append this section verbatim to each consumer repo's AGENTS.md.

## Logging compliance (SOC2)

Logs MUST carry no PII, credentials, or raw payloads. Enforced by the `soc2-logging`
pre-commit hook and a required CI check (rules:
[finelo-subpilot/compliance-rules](https://github.com/finelo-subpilot/compliance-rules)).
Log **opaque ids only** — names suffixed `_id` are always allowed.

| Banned in any log call | Instead |
|------------------------|---------|
| `logger.info('event', payload=payload.model_dump())` | `logger.info('event', user_id=payload.user_id)` |
| `logger.info('webhook', payload=payload)` / `data=data` / `event=event` | `logger.info('webhook', webhook_code=payload.webhook_code)` |
| `logger.info(f'session: {session_token}')` / `access_token=token` | `logger.info('session reused', user_id=user_id)` or `has_token=bool(token)` |
| `logger.info('sent', email=email)` / f-string `{email}` (denylist: email, phone, address, names, dob, card*, ssn, ip, sender, subject, snippet, body, lat/lon) | `logger.info('sent', email_id=message.email_id)` |
| `logger.error(f'api error: {response.text}')` | `logger.error('api error', status_code=response.status_code)` |
| `console.log('checkout', user)` / whole `payload`/`session`/`req.body` objects | `console.log('checkout', user.id)` |

False positive? Suppress narrowly, with the rule id and a mandatory justification on
the same line (this is the SOC2 exceptions register — bare `nosemgrep` is forbidden):

```python
logger.info('gateway reply', body=scrubbed)  # nosemgrep: soc2-logging.python.no-pii-fields-in-logs — scrubbed by gateway_sanitize(), TICKET-1234
```

Use the short id from the rule (`soc2-logging.<lang>.<slug>`), not the path-prefixed
form CI may display. Extra paths to skip (generated code etc.) go in a repo-local
`.semgrepignore`.
