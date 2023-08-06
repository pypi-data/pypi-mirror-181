import pandas as pd
import requests
import socket
import logging
import json
from .models import VintexData
from .models import Qc0020Response
from .models import Qc0021Response
from urllib.parse import urlunparse

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
    SYSTEM_ID = 79
    PROTOCOL = "http"
    HOSTNAME = "10.189.100.162"
    PORT = 48081

    HEADERS = {"Content-Type": "application/json"}

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

    def __init__(self, custid: str, auth: str):
        logger.debug("Initializing GTJA Qyt Python lib...")

        self.ip = GTJAVintexQyt._get_ip()
        logger.debug(f"Client ip: {self.ip}.")

        self.customer_id = custid
        self.auth_code = auth

    @staticmethod
    def qc0020(
            page: int = 1,
            rownum: int = 10000,
            pooltype: str = None
    ) -> VintexData:
        logger.debug(f"Calling qc0020. page: {page}, rownum: {rownum}, pooltype: {pooltype}.")

        path = "/api/v1/qyt/QC/QC0020"

        payload = {}

        if pooltype:
            payload["businessInfo"]["vc_type"] = pooltype

        url = urlunparse(
            (GTJAVintexQyt.PROTOCOL, f"{GTJAVintexQyt.HOSTNAME}:{GTJAVintexQyt.PORT}", path, None, None, None))

        # Since max row num of qyt backend api is 500, but qyt team set the default row num of pytho sdk to 10000.
        # We need to do multiple queries to the server.
        # And please DO NOT ask why the start index of page is 1. Please ask qyt backend team for the reason.
        current_index = (page - 1) * rownum
        end_index = page * rownum

        logger.debug(f"result start_index: {current_index}, end_index: {end_index}.")

        data = pd.DataFrame()
        vintex_data = VintexData(0, 0, "", None)

        while current_index < end_index:
            query_row_num = min(500, rownum)
            logger.debug(f"do query from {current_index} to {query_row_num + current_index}.")

            try:
                payload["pag"] = int(current_index / query_row_num) + 1
                payload["rownum"] = query_row_num
                r = requests.post(url, data=json.dumps(payload), headers=GTJAVintexQyt.HEADERS)

                if r.status_code != 200:
                    logger.error("")

                query_data = []

                # Please ask qyt backend team why 0 stands for having error.
                if r.json()["code"] == 0:
                    return VintexData(-1, r.json()["msg"], r.json()["total"], None)

                vintex_data.msg = r.json()["msg"]
                vintex_data.total_num = r.json()["total"]

                for d in r.json()["data"]:
                    if current_index >= end_index:
                        break

                    query_data.append(
                        Qc0020Response(d["market"],
                                       d["floorrate"],
                                       d["stkcode"],
                                       d["stkname"],
                                       d["reslimit"],
                                       d["startdate"],
                                       d["limitdate"],
                                       d["totalleftqty"])
                    )
                    current_index += 1

                data = pd.concat([data, pd.DataFrame(query_data)])

            except Exception as e:
                logger.error((e))

        vintex_data.data = data
        return vintex_data

    @staticmethod
    def qc0021(
            custid: str = "2933102",
            page: int = 1,
            rownum: int = 10000,
            pooltype: str = None
    ) -> VintexData:
        logger.debug(f"Calling qc0021. page: {page}, rownum: {rownum}, pooltype: {pooltype}.")

        path = "/api/v1/qyt/QC/QC0021"

        payload = {"custid": custid}

        if pooltype:
            payload["businessInfo"]["vc_type"] = pooltype

        url = urlunparse(
            (GTJAVintexQyt.PROTOCOL, f"{GTJAVintexQyt.HOSTNAME}:{GTJAVintexQyt.PORT}", path, None, None, None))

        # Since max row num of qyt backend api is 500, but qyt team set the default row num of pytho sdk to 10000.
        # We need to do multiple queries to the server.
        # And please DO NOT ask why the start index of page is 1. Please ask qyt backend team for the reason.
        current_index = (page - 1) * rownum
        end_index = page * rownum

        logger.debug(f"result start_index: {current_index}, end_index: {end_index}.")

        data = pd.DataFrame()
        vintex_data = VintexData(0, 0, "", None)

        while current_index < end_index:
            query_row_num = min(500, rownum)
            logger.debug(f"do query from {current_index} to {query_row_num + current_index} ")

            try:
                payload["pag"] = int(current_index / query_row_num) + 1
                payload["rownum"] = query_row_num

                r = requests.post(url, data=json.dumps(payload), headers=GTJAVintexQyt.HEADERS)

                if r.status_code != 200:
                    logger.error("")

                vintex_data.msg = r.json()["msg"]
                vintex_data.total_num = r.json()["total"]

                query_data = []

                # Please ask qyt backend team why 0 stands for having error.
                if r.json()["code"] == 0:
                    return VintexData(-1, r.json()["msg"], r.json()["total"], None)

                for d in r.json()["data"]:
                    if current_index >= end_index:
                        break

                    query_data.append(
                        Qc0021Response(d["market"],
                                       d["floorrate"],
                                       d["stkcode"],
                                       d["stkname"],
                                       d["actualleftqty"],
                                       d["startdate"])
                    )
                    current_index += 1

                data = pd.concat([data, pd.DataFrame(query_data)])

            except Exception as e:
                logger.error((e))

        vintex_data.data = data
        return vintex_data
