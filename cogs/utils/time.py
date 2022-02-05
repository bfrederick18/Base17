import cogs.utils.constants as c
import math

from datetime import datetime


def now():
    return f'{datetime.now(c.tz).strftime("%Y/%m/%d %H:%M:%S")} {str(math.trunc(int(datetime.now(c.tz).strftime("%f")) / 100)).zfill(4)}'
