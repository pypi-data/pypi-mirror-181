import json
import logging
import socket
import sys

import pandas as pd
import requests

from .gtja_vintex_requests import GtjaVintexRequests
from .models import Qc0020Response
from .models import Qc0021Response
from .models import VintexData

formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

logger = logging.getLogger()
logging_level = logging.DEBUG

logger.setLevel(logging_level)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.DEBUG)

logger.addHandler(ch)

fh = logging.FileHandler("gtja_qyt.log", "a", encoding="utf-8")
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


class GTJAVintexQyt:
    @staticmethod
    def _get_ip():
        try:
            logger.debug("Trying to get external ip from ipify.org...")
            r = requests.get("https://api.ipify.org?format=json")
            return r.json()["ip"]
        except Exception:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0)
            try:
                s.connect(("10.254.254.254", 1))
                return s.getsockname()[0]
            except Exception:
                return "127.0.0.1"
            finally:
                s.close()

    def __init__(self, vintex_username: str, vintex_password: str):
        logger.debug("Initializing GTJA Vintex Qyt Python SDK...")

        if not GtjaVintexRequests.login(vintex_username, vintex_password):
            sys.exit(-1)

    @staticmethod
    def qc0020(
            custid: int = 2933102,
            fundid: int = 1689971,
            page: int = 1,
            rownum: int = 10000,
            pooltype: str = None
    ) -> VintexData:
        logger.debug(
            f"Calling qc0020. custid: {custid}, fundid: {fundid}, page: {page}, rownum: {rownum}, pooltype: {pooltype}.")

        path = "/api/v1/qyt/QC/QC0020"

        payload = {
            "custid": custid
        }

        if pooltype:
            payload["vc_type"] = pooltype

        # Since max row num of qyt backend api is 500, but qyt team set the default row num of pytho sdk to 10000.
        # We need to do multiple queries to the server.
        # And please DO NOT ask why the start index of page is 1. Please ask qyt backend team for the reason.
        current_index = (page - 1) * rownum
        end_index = page * rownum

        total = sys.maxsize

        logger.debug(f"result start_index: {current_index}, end_index: {end_index}.")

        data = pd.DataFrame()
        vintex_data = VintexData(0, 0, "", None)

        while current_index < end_index and current_index < total:
            query_row_num = min(500, rownum)
            logger.debug(f"do query from {current_index} to {query_row_num + current_index}.")

            try:
                payload["pag"] = int(current_index / query_row_num) + 1
                payload["rownum"] = query_row_num
                r = GtjaVintexRequests.post(path, json.dumps(payload, indent=4))

                if r.status_code != 200:
                    logger.error("券源通服务器错误。")

                query_data = []

                # Please ask qyt backend team why 0 stands for having error.
                if r.json()["code"] == 0:
                    return VintexData(-1, r.json()["msg"], r.json()["total"], None)

                total = r.json()["total"]

                vintex_data.msg = r.json()["msg"]
                vintex_data.total_num = r.json()["total"]

                for d in r.json()["data"]:
                    if current_index >= end_index:
                        break

                    query_data.append(
                        Qc0020Response(d["stkcode"],
                                       d["stkname"],
                                       d["totalleftqyt"],
                                       d["floorrate"],
                                       d["reslimit"],
                                       d["vc_type"])
                    )
                    current_index += 1

                data = pd.concat([data, pd.DataFrame(query_data)])

            except Exception as e:
                logger.error(e)

        vintex_data.data = data
        return vintex_data

    @staticmethod
    def qc0021(
            custid: int = 2933102,
            fundid: int = 1689971,
            page: int = 1,
            rownum: int = 10000,
            pooltype: str = None
    ) -> VintexData:
        logger.debug(
            f"Calling qc0021. page: {page}, rownum: {rownum}, custid: {custid}, fundid: {fundid}, pooltype: {pooltype}.")

        path = "/api/v1/qyt/QC/QC0021"

        payload = {"custid": custid}

        if pooltype:
            payload["businessInfo"]["vc_type"] = pooltype

        # Since max row num of qyt backend api is 500, but qyt team set the default row num of pytho sdk to 10000.
        # We need to do multiple queries to the server.
        # And please DO NOT ask why the start index of page is 1. Please ask qyt backend team for the reason.
        current_index = (page - 1) * rownum
        end_index = page * rownum

        logger.debug(f"result start_index: {current_index}, end_index: {end_index}.")

        data = pd.DataFrame()
        vintex_data = VintexData(0, 0, "", None)

        total = sys.maxsize

        while current_index < end_index and current_index < total:
            query_row_num = min(500, rownum)
            logger.debug(f"do query from {current_index} to {query_row_num + current_index} ")

            try:
                payload["pag"] = int(current_index / query_row_num) + 1
                payload["rownum"] = query_row_num

                r = GtjaVintexRequests.post(path, json.dumps(payload, indent=4))

                if r.status_code != 200:
                    logger.error("券源通服务器错误。")

                vintex_data.msg = r.json()["msg"]
                vintex_data.total_num = r.json()["total"]

                query_data = []

                # Please ask qyt backend team why 0 stands for having error.
                if r.json()["code"] == 0:
                    return VintexData(-1, r.json()["msg"], r.json()["total"], None)

                total = r.json()["total"]

                for d in r.json()["data"]:
                    if current_index >= end_index:
                        break

                    query_data.append(
                        Qc0021Response(d["stkcode"],
                                       d["stkname"],
                                       d["actualleftqty"],
                                       d["floorrate"])
                    )
                    current_index += 1

                data = pd.concat([data, pd.DataFrame(query_data)])

            except Exception as e:
                logger.error(e)

        vintex_data.data = data
        return vintex_data
