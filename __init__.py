import hashlib
import hmac
import pickle
import logging
import logging.handlers
import socketserver
import struct
import os
import time

import config

VERSION = "1.0"
svr_logger = logging.getLogger("logging_svr")

if os.environ.get('LOG_SVR_ENV', '') == 'production':
    app_config = config.ProdConfig
else:
    app_config = config.DevConfig


class LogRecordStreamHandler(socketserver.StreamRequestHandler):
    """Handler for a streaming logging request.

    This basically logs the record using whatever logging policy is
    configured locally.
    """

    def handle(self):
        """
        Handle multiple requests - each expected to be a 36-bytes length,
        followed by the LogRecord in pickle format. Logs the record
        according to whatever policy is configured locally.
        """
        while True:
            header = self.connection.recv(36)
            if len(header) < 36:
                break
            slen, data_digest = struct.unpack('!L32s', header)
            data = self.connection.recv(slen)
            while len(data) < slen:
                data = data + self.connection.recv(slen - len(data))

            # Check the data digest of the message
            golden_digest = hmac.new(app_config.LOG_SVR_DIGEST_KEY, data, hashlib.sha256).digest()
            if hmac.compare_digest(data_digest, golden_digest):
                # Create log entry
                obj = self.unPickle(data)
                record = logging.makeLogRecord(obj)
                self.handleLogRecord(record)
            else:
                # Discard message
                svr_logger.error(f"Connection from [{self.connection.getpeername()[0]}:{self.connection.getpeername()[1]}] - failed digest check and message discarded")

    def unPickle(self, data):
        return pickle.loads(data)

    def handleLogRecord(self, record):
        # if a name is specified, we use the named logger rather than the one
        # implied by the record.
        if self.server.logname is not None:
            name = self.server.logname
        else:
            name = record.name
        logger = logging.getLogger(name)
        # N.B. EVERY record gets logged. This is because Logger.handle
        # is normally called AFTER logger-level filtering. If you want
        # to do filtering, do it at the client end to save wasting
        # cycles and network bandwidth!
        logger.handle(record)


class LogRecordSocketReceiver(socketserver.ThreadingTCPServer):
    """
    Simple TCP socket-based logging receiver suitable for testing.
    """

    allow_reuse_address = True

    def __init__(self, host=app_config.LOG_SVR_IP,
                 port=app_config.LOG_SVR_PORT,
                 handler=LogRecordStreamHandler):
        socketserver.ThreadingTCPServer.__init__(self, (host, port), handler)
        self.abort = 0
        self.timeout = 1
        self.logname = None

    def serve_until_stopped(self):
        import select
        abort = 0
        while not abort:
            rd, wr, ex = select.select([self.socket.fileno()],
                                       [], [],
                                       self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort


def main():

    if app_config.LOG_SVR_DEBUG:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    handler = logging.handlers.RotatingFileHandler(app_config.LOG_SVR_FILE,
                                                   maxBytes=200000,
                                                   backupCount=1)
    formatter = logging.Formatter('%(asctime)s  %(name)-15s [%(levelname)s] %(message)s')
    formatter.converter = time.gmtime
    handler.setFormatter(formatter)

    logging.basicConfig(format='%(asctime)s  %(name)-15s [%(levelname)s] %(message)s',
                        handlers=[handler],
                        level=log_level)

    tcpserver = LogRecordSocketReceiver()
    svr_logger.info(f"-- Logging Server Version {VERSION} --")
    svr_logger.info(f"Detected environment: {app_config.LOG_SVR_ENV}")
    svr_logger.info(f"Binding to: {app_config.LOG_SVR_IP}:{app_config.LOG_SVR_PORT}")
    if app_config.LOG_SVR_DEBUG:
        svr_logger.info(f"Debug logging: Enabled")
    else:
        svr_logger.info(f"Debug logging: Disabled")
    tcpserver.serve_until_stopped()


if __name__ == '__main__':
    main()
