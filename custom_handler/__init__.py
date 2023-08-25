import hashlib
import logging.handlers
import hmac
import pickle
import struct
from os import environ

LOG_SVR_DIGEST_KEY = str.encode(environ.get('LOG_SVR_DIGEST_KEY'))

class SocketHandlerHMAC(logging.handlers.SocketHandler):

    def makePickle(self, record: logging.LogRecord) -> bytes:
        SECRET_KEY = LOG_SVR_DIGEST_KEY
        data = pickle.dumps(record.__dict__, 1)
        digest = hmac.new(SECRET_KEY, data, hashlib.sha256).digest()
        header = struct.pack('!L32s', len(data), digest)
        return header + data