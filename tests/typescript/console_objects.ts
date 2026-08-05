// Fixtures for soc2-logging.typescript.no-object-dumps-in-logs. All data invented.

function handleCheckout(user: User, payload: Payload, session: Session, req: Request) {
  // ruleid: soc2-logging.typescript.no-object-dumps-in-logs
  console.log('checkout started', user);

  // ruleid: soc2-logging.typescript.no-object-dumps-in-logs
  console.error('payment failed', payload);

  // ruleid: soc2-logging.typescript.no-object-dumps-in-logs
  logger.info('session state', session);

  // ruleid: soc2-logging.typescript.no-object-dumps-in-logs
  console.debug('incoming request', req.body);

  // ruleid: soc2-logging.typescript.no-object-dumps-in-logs
  console.log('checkout snapshot', { ...user });

  // ok: soc2-logging.typescript.no-object-dumps-in-logs
  console.log('checkout started', user.id);

  // ok: soc2-logging.typescript.no-object-dumps-in-logs
  logger.info('session state', { userId: session.userId });
}
