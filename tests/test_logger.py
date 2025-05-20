import logging


def test_echo_logger():
    logger = logging.getLogger("test")
    logger.info("test")
    logger.error("test")
    logger.warning("test")
    logger.debug("test")
    logger.critical("test")
    logger.fatal("test")
    logger.exception("test")
    logger.warning("test")
