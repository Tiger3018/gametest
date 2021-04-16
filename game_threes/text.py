import logging


def logwarn(strIn : str):
    logging.warning(strIn)
def loginfo(strIn : str):
    logging.info(strIn)

def __init__():
    logging.basicConfig(format = "%(threadName)s - [%(levelname)s] %(message)s")
    logging.getLogger().setLevel(logging.INFO)

__init__()