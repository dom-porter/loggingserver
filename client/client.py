import logging.handlers

from handler import SocketHandlerHMAC

rootLogger = logging.getLogger('')
rootLogger.setLevel(logging.DEBUG)

socketHandler = SocketHandlerHMAC('localhost',
                    logging.handlers.DEFAULT_TCP_LOGGING_PORT)
# don't bother with a formatter, since a socket handler sends the event as
# an unformatted pickle
rootLogger.addHandler(socketHandler)

# Root logger
logging.info('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua')

# application:

logger1 = logging.getLogger('myapp.area1')
logger2 = logging.getLogger('myapp.area2')

logger1.debug('Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.')
logger1.info('Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')
logger2.warning('Arcu vitae elementum curabitur vitae nunc sed velit.')
logger2.error('At ultrices mi tempus imperdiet nulla. Vestibulum rhoncus est pellentesque elit ullamcorper dignissim.')