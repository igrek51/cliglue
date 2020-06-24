from nuclear.sublog import log_error, log, context_logger, root_context_logger
from tests.asserts import MockIO


def test_context_logger():
    with MockIO() as mockio:
        with context_logger(request_id=0xdeaddead) as logger:
            logger.debug('got request')
            with context_logger(logger, user='igrek') as logger2:
                logger2.info('logged in', page='sweet home')
                log.warn('im a root')

            logger.debug('logged out')
        log.debug('exited')

        # datetime
        mockio.assert_match('^\\[\x1b\\[0;36m\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}\x1b\\[0m\\] ')
        # log level
        mockio.assert_match(' \\[\x1b\\[0;32mDEBUG\x1b\\[0m\\] ')
        # message with context
        mockio.assert_match(' got request \x1b\\[0;32mrequest_id=\x1b\\[1;32m3735936685\x1b\\[0m$')

        mockio.assert_match_uncolor('] logged in request_id=3735936685 user=igrek page="sweet home"$')
        mockio.assert_match_uncolor('] im a root$')
        mockio.assert_match_uncolor('] logged out request_id=3735936685$')
        mockio.assert_match_uncolor('] exited$')


def test_root_context_logger():
    with MockIO() as mockio:
        log.debug('outside context', a=4)

        with root_context_logger(request_id=0xdeaddead):
            log.debug('got request')

            with root_context_logger(user='igrek'):
                log.info('logged in', page='home')
                with log_error():
                    log.warn('im a root')
                    raise RuntimeError("I'm a pickle")

            log.debug('logged out')

        log.debug('exited')

        mockio.assert_match_uncolor('] outside context a=4$')
        mockio.assert_match_uncolor('] got request request_id=3735936685$')
        mockio.assert_match_uncolor('] logged in request_id=3735936685 user=igrek page=home$')
        mockio.assert_match_uncolor('] im a root request_id=3735936685 user=igrek$')
        mockio.assert_match_uncolor('] I\'m a pickle request_id=3735936685 user=igrek$')
        mockio.assert_match_uncolor('] logged out request_id=3735936685$')
        mockio.assert_match_uncolor('] exited$')