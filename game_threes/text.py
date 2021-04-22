import logging

def logerror(*strIn ):
    logging.error(strIn)
def logwarn(*strIn ):
    logging.warning(strIn)
def loginfo(*strIn ):
    logging.info(strIn)
def logdebug(*strIn ):
    logging.debug(strIn)

def __init__():
    logging.basicConfig(format = "[%(levelname)s] %(threadName)s - %(message)s")
    logging.getLogger().setLevel(logging.INFO)

__init__()