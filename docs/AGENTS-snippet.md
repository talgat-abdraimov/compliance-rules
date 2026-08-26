# Logging compliance (SOC2)

> Append this section verbatim to each consumer repo's AGENTS.md.

## Logging compliance (SOC2)

Logs MUST carry no PII, credentials, or raw payloads. Enforced by the `soc2-logging`
pre-commit hook and a required CI check (rules:
[talgat-abdraimov/compliance-rules](https://github.com/talgat-abdraimov/compliance-rules)).
Log **opaque ids only** — names suffixed `_id`/`Id` are always allowed (except identity
documents: `national_id`, `passport_id`, `tax_id`).

| Banned in any log call | Instead |
|------------------------|---------|
| `logger.info('event', payload=payload.model_dump())` / `.dict()` / `vars(user)` / `json.dumps(payload)` | `logger.info('event', user_id=payload.user_id)` |
| `logger.info('webhook', payload=payload)` / `data=data` / `event=event` / positional `logger.info('webhook', payload)` / `f'{payload}'` / `extra={'payload': payload}` | `logger.info('webhook', webhook_code=payload.webhook_code)` |
| `logger.info(f'session: {session_token}')` / `access_token=token` / `logger.info('auth: %s', token)` | `logger.info('session reused', user_id=user_id)` or `has_token=bool(token)` |
| `logger.info('sent', email=email)` / `phone_number=…` / `logger.info('sent to %s', email)` / f-string `{email}` (denylist: email, phone\*, address\*, names, dob, card\*, ssn, passport\*, iban, ip, sender, subject, snippet, body, lat/lon/latitude/longitude) | `logger.info('sent', email_id=message.email_id)` |
| `logger.error(f'api error: {response.text}')` / `.content` / `.json()` | `logger.error('api error', status_code=response.status_code)` |
| `console.log('checkout', user)` / whole `payload`/`session`/`req.body` / `{ email }` shorthand / `JSON.stringify(user)` / `console.table(rows)` | `console.log('checkout', user.id)` |

Counts, lengths, hashes and booleans are fine: `email_count`, `len(body)`, `has_token`,
`address_hash`, `prompt_tokens`/`max_tokens` (LLM token counts), `secret_name`.

False positive? Suppress narrowly, with the rule id and a mandatory justification on
the same line (this is the SOC2 exceptions register — bare `nosemgrep` is forbidden and
fails CI):

```python
logger.info('gateway reply', body=scrubbed)  # nosemgrep: soc2-logging.python.no-pii-fields-in-logs — scrubbed by gateway_sanitize(), TICKET-1234
```

Use the short id from the rule (`soc2-logging.<lang>.<slug>`), not the path-prefixed
form CI may display. To skip whole paths (generated code etc.), add `exclude:` to the
hook in `.pre-commit-config.yaml` — semgrep ignores `.semgrepignore` and `--exclude`
for explicitly passed filenames, so `.semgrepignore` affects only the CI directory scan.

Not covered by the gate — review these yourself: `print(...)` (stdout is a log stream),
string concatenation (`'to ' + email`), and values carried inside exceptions
(`logger.error(f'{e}')` where a validation error embeds its input).
