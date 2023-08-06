from datetime import datetime

import pandas as pd

from dataclasses import dataclass


class VintexData:
    ERROR_DICT = {
        -2: "连接券源通错误"
    }

    def __init__(self,
                 error_code: int,
                 total_num: int,
                 msg: str,
                 data: pd.DataFrame):
        self.error_code = error_code
        self.total_num = total_num
        self.msg = msg
        self.data = data


@dataclass
class Qc0020Response:
    market: str
    sblrate: float
    stkcode: str
    stkname: str
    reslimit: int
    startdate: datetime
    enddate: datetime
    totalqty: int


@dataclass
class Qc0021Response:
    market: str
    sblrate: float
    stkcode: str
    stkname: str
    realqty: int
    startdate: datetime
