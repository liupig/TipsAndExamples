import logging
import datetime
from pytz import timezone, utc


def gmt8(*args):
    utc_dt = utc.localize(datetime.datetime.utcnow())
    my_tz = timezone("Asia/Shanghai")
    converted = utc_dt.astimezone(my_tz)
    return converted.timetuple()


SERVICE_NAME = "SERVICE_SIGN"
LOG_FORMAT = f"{SERVICE_NAME} %(asctime)s %(levelname)s [%(threadName)s] %(funcName)s [%(filename)s:%(lineno)d] " \
             f"tradeId- span- - %(message)s"

logging.Formatter.converter = gmt8
logging.Formatter.default_msec_format = '%s.%03d'
logging.basicConfig(format=LOG_FORMAT)
LOG = logging.getLogger("all_log")
# one can set the level to debug when doing it
LOG.setLevel(level=logging.INFO)
