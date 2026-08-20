// Fixtures for soc2-logging.typescript.no-pii-fields-in-logs. All data invented.

function notify(email: string, user: User, message: Msg, body: string) {
  // ruleid: soc2-logging.typescript.no-pii-fields-in-logs
  console.log('sending to', email);

  // ruleid: soc2-logging.typescript.no-pii-fields-in-logs
  console.info(`magic link for ${email}`);

  // ruleid: soc2-logging.typescript.no-pii-fields-in-logs
  logger.warn('detection event', { sender: message.sender });

  // ruleid: soc2-logging.typescript.no-pii-fields-in-logs
  console.log('card check', user.cardNumber);

  // Shorthand properties hide the same value.
  // ruleid: soc2-logging.typescript.no-pii-fields-in-logs
  console.log('sending to', { email });

  // ruleid: soc2-logging.typescript.no-pii-fields-in-logs
  console.log('sms queued', { phoneNumber: user.phoneNumber });

  // An innocent key with a PII value is still PII.
  // ruleid: soc2-logging.typescript.no-pii-fields-in-logs
  console.log('actor resolved', { actor: user.email });

  // camelCase and snake_case denylist hits.
  // ruleid: soc2-logging.typescript.no-pii-fields-in-logs
  console.log('geo', { latitude: user.latitude, longitude: user.longitude });

  // ruleid: soc2-logging.typescript.no-pii-fields-in-logs
  console.log('client info', { ipAddress: user.ipAddress });

  // ruleid: soc2-logging.typescript.no-pii-fields-in-logs
  console.log('kyc submitted', { nationalId: user.nationalId });

  // winston/pino levels and logger aliases.
  // ruleid: soc2-logging.typescript.no-pii-fields-in-logs
  logger.verbose('sending to', { email });

  // ruleid: soc2-logging.typescript.no-pii-fields-in-logs
  LOGGER.info('sending to', user.email);

  // ok: soc2-logging.typescript.no-pii-fields-in-logs
  console.log('notification sent', { emailId: message.emailId });

  // ok: soc2-logging.typescript.no-pii-fields-in-logs
  console.log('notification sent', message.emailId);

  // ok: soc2-logging.typescript.no-pii-fields-in-logs
  console.log('digest built', { emailCount: 3, hasEmail: true, addressHash: user.addressHash });

  // ok: soc2-logging.typescript.no-pii-fields-in-logs
  console.log('received bytes', body.length);

  // ok: soc2-logging.typescript.no-pii-fields-in-logs
  console.log('upstream latency', { p99Lat: 42.0 });

  // "pan" must not match inside unrelated words.
  // ok: soc2-logging.typescript.no-pii-fields-in-logs
  console.log('region resolved', { japan: true });

  // Quoted constants are literals, not the user's data.
  // ok: soc2-logging.typescript.no-pii-fields-in-logs
  console.log('notification queued', { channel: 'email' });

  // ok: soc2-logging.typescript.no-pii-fields-in-logs
  sendEmail(email);
}
