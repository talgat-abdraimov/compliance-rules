// Fixtures for soc2-logging.typescript.no-pii-fields-in-logs. All data invented.

function notify(email: string, user: User, message: Msg) {
  // ruleid: soc2-logging.typescript.no-pii-fields-in-logs
  console.log('sending to', email);

  // ruleid: soc2-logging.typescript.no-pii-fields-in-logs
  console.info(`magic link for ${email}`);

  // ruleid: soc2-logging.typescript.no-pii-fields-in-logs
  logger.warn('detection event', { sender: message.sender });

  // ruleid: soc2-logging.typescript.no-pii-fields-in-logs
  console.log('card check', user.cardNumber);

  // ok: soc2-logging.typescript.no-pii-fields-in-logs
  console.log('notification sent', { emailId: message.emailId });

  // ok: soc2-logging.typescript.no-pii-fields-in-logs
  console.log('notification sent', message.emailId);

  // ok: soc2-logging.typescript.no-pii-fields-in-logs
  sendEmail(email);
}
