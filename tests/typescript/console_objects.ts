// Fixtures for soc2-logging.typescript.no-object-dumps-in-logs. All data invented.

function handleCheckout(user: User, payload: Payload, session: Session, req: Request, users: User[]) {
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

  // Serializing the object is still dumping the object.
  // ruleid: soc2-logging.typescript.no-object-dumps-in-logs
  console.log('checkout snapshot', JSON.stringify(user));

  // ruleid: soc2-logging.typescript.no-object-dumps-in-logs
  console.log(`checkout snapshot: ${JSON.stringify(payload)}`);

  // console.table/dir dump everything they are given.
  // ruleid: soc2-logging.typescript.no-object-dumps-in-logs
  console.table(users);

  // ruleid: soc2-logging.typescript.no-object-dumps-in-logs
  console.dir(user);

  // ok: soc2-logging.typescript.no-object-dumps-in-logs
  console.log('checkout started', user.id);

  // ok: soc2-logging.typescript.no-object-dumps-in-logs
  logger.info('session state', { userId: session.userId });

  // An inline literal names its own fields — nothing is dumped wholesale.
  // ok: soc2-logging.typescript.no-object-dumps-in-logs
  console.log('audit', JSON.stringify({ userId: session.userId }));
}
