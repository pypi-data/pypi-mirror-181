from dataclasses import dataclass

import pandas as pd


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
    stkcode: str
    stkname: str
    totalqty: int
    sblrate: float
    reslimit: int
    pooltype: str


@dataclass
class Qc0021Response:
    stkcode: str
    stkname: str
    realqty: int
    sblrate: float
