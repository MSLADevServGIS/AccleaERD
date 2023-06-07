from logger import make_logger
from dbconnections import AccelaProd, AccelaNonProd1, AccelaNonProd2

e = None

logger = make_logger(__file__)


logger.info("Connecting to Prod...")
try:
    prod = AccelaProd.connect()
    logger.info("  Connected.")
except Exception as e:
    logger.error(e)

logger.info("Connecting to NonProd1...")
try:
    np1 = AccelaNonProd1.connect()
    logger.info("  Connected.")
except Exception as e:
    logger.error(e)

logger.info("Connecting to NonProd2...")
try:
    np2 = AccelaNonProd1.connect()
    logger.info("  Connected.")
except Exception as e:
    logger.error(e)

if not e:
    logger.info("Complete")
