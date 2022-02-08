import math

from config import tz
from datetime import datetime


def now():
    return f'{datetime.now(tz).strftime("%Y/%m/%d %H:%M:%S")} {str(math.trunc(int(datetime.now(tz).strftime("%f")) / 100)).zfill(4)}'
