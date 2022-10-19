import hashlib
import logging
import logging.handlers
import hmac
import pickle
import struct


class SocketHandlerHMAC(logging.handlers.SocketHandler):

    def makePickle(self, record: logging.LogRecord) -> bytes:
        SECRET_KEY = str.encode("fszfifc68lagw89iml77l")
        data = pickle.dumps(record.__dict__, 1)
        digest = hmac.new(SECRET_KEY, data, hashlib.sha256).digest()
        header = struct.pack('!L32s', len(data), digest)
        return header + data


rootLogger = logging.getLogger('')
rootLogger.setLevel(logging.DEBUG)
# socketHandler = logging.handlers.SocketHandler('localhost',
                    # logging.handlers.DEFAULT_TCP_LOGGING_PORT)

socketHandler = SocketHandlerHMAC('localhost',
                    logging.handlers.DEFAULT_TCP_LOGGING_PORT)
# don't bother with a formatter, since a socket handler sends the event as
# an unformatted pickle
rootLogger.addHandler(socketHandler)

# Now, we can log to the root logger, or any other logger. First the root...
logging.info('Jackdaws love my big sphinx of quartz.')

# Now, define a couple of other loggers which might represent areas in your
# application:

logger1 = logging.getLogger('myapp.area1')
logger2 = logging.getLogger('myapp.area2')

logger1.debug('Quick zephyrs blow, vexing daft Jim.')
logger1.info('How quickly daft jumping zebras vex.')
logger2.warning('Jail zesty vixen who grabbed pay from quack.')
logger2.error('The five boxing wizards jump quickly.')