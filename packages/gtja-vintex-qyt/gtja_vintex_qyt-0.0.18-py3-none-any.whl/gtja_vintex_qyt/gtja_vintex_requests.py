import ctypes
import json
import logging
import pathlib
from ctypes import *
from urllib.parse import urlunparse

import requests

from .constants import Constants
from .utils import Utils

logger = logging.getLogger()


class GtjaVintexRequests(object):
    SYSTEM_ID = 79

    PROTOCOL = "https"

    HOST = "101.231.93.226"
    PORT = 8050

    HEADERS_TEMPLATE = {
        "App-Name": "daoheallused",
        "App-ID": "7A278FCFAE732E4CFBF9981EE7592534",
        "Session-ID": Utils.SESSION_ID,
        "Device-ID": Utils.get_device_id(),
        "Ant-ID": "",
        "Aes-ID": "",
        "Verify-ID": "",
        "Content-Type": "application/json",
        "Platform": "pc",
        "Model-Type": "",
        "System-Version": Utils.get_system_version(),
        "App-Channel": "gtja-vintex-qyt-python-sdk",
        "App-Version": Constants.version,
        "Terminal-Type": "pc",
        "Jwt-Assertion": ""
    }

    LOGIN_JWT_TOKEN = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsidmludGV4LnZpc2l0b3IiXSwiZXhwIjoxOTg1MDY0NDA1LCJpYXQiOjE2Njk3MDQ0MDUsImlzcyI6ImF1YyIsInN1YiI6InZpbnRleCIsInVzZXJjb2RlIjoiMjY3NTU0MiJ9.aoo4nR_90GxHiHK3zvaPx5aBXj920Z_ogGw2FCwEVtGUiilhbmQj839DWZ7X_thSerRfyeCJUUxlF6yzLdR0ZA"

    @staticmethod
    def get_gtja_common_lib() -> CDLL:
        if Constants.os == "Windows":
            return ctypes.CDLL(str(pathlib.Path(__file__).parent.resolve() / 'lib' / 'libGtjaCommon.dll'))
        elif Constants.os == "Linux":
            return ctypes.CDLL(str(pathlib.Path(__file__).parent.resolve() / 'lib' / 'libGtjaCommon.so'))

    @staticmethod
    def gen_new_aes_id(session_id: str, ant_id: str) -> str:
        lib = GtjaVintexRequests.get_gtja_common_lib()
        lib.genNewAesId.restype = c_char_p
        return lib.genNewAesId(session_id.encode("utf-8"), ant_id.encode("utf-8")).decode()

    @staticmethod
    def gen_verify_id(body: str) -> str:
        lib = GtjaVintexRequests.get_gtja_common_lib()
        lib.genVerifyId.restype = c_char_p
        body_bytes = str.encode(body)
        return lib.genVerifyId(body_bytes, len(body_bytes)).decode("utf-8")

    @staticmethod
    def gen_ant_id() -> str:
        lib = GtjaVintexRequests.get_gtja_common_lib()
        lib.genAntId.restype = c_char_p
        return lib.genAntId().decode()

    @staticmethod
    def login(mobile_number: str, password: str) -> None:
        headers = GtjaVintexRequests.HEADERS_TEMPLATE

        body = json.dumps({
            "loginType": "1",
            "passwordZC": Utils.encrypt_with_vintex_rsa(password),
            "mobileNo": Utils.encrypt_with_vintex_aes(mobile_number),
            "mobileUserCode": "0",
            "deviceId": Utils.get_device_id(),
            "terminalSource": "106"
        }, indent=4)

        headers["Ant-ID"] = GtjaVintexRequests.gen_ant_id()
        headers["Aes-ID"] = GtjaVintexRequests.gen_new_aes_id('pc', headers["Ant-ID"])
        headers["Verify-ID"] = GtjaVintexRequests.gen_verify_id(body)
        headers["Jwt-Assertion"] = GtjaVintexRequests.LOGIN_JWT_TOKEN

        url = urlunparse(
            (GtjaVintexRequests.PROTOCOL, f"{GtjaVintexRequests.HOST}:{GtjaVintexRequests.PORT}",
             "/organ/login/v1/80000002", None, None, None))

        # TODO: enable ssl check
        r = requests.post(url=url, data=body, headers=headers, verify=False)

        if r.status_code != 200:
            logger.error("连接道合服务器错误。")
            logger.debug(r.content)
            return False

        result_json = json.loads(r.text)

        if result_json["msg"] != "Success" and result_json["status"] != "0":
            logger.error(result_json["msg"])
            return False

        # TODO： re-enable jwt token replacement after vintex team fix their issue.
        # GtjaVintexRequests.HEADERS_TEMPLATE["Jwt-Assertion"] = result_json["data"]["jwtToken"]
        return True

    @staticmethod
    def post(path: str, body: str) -> requests.models.Response:
        headers = GtjaVintexRequests.HEADERS_TEMPLATE

        headers["Ant-ID"] = GtjaVintexRequests.gen_ant_id()
        headers["Aes-ID"] = GtjaVintexRequests.gen_new_aes_id(headers["Session-ID"], headers["Ant-ID"])
        headers["Verify-ID"] = GtjaVintexRequests.gen_verify_id(body)

        url = urlunparse(
            (GtjaVintexRequests.PROTOCOL, f"{GtjaVintexRequests.HOST}:{GtjaVintexRequests.PORT}",
             path, None, None, None))

        # TODO: enable ssl check
        r = requests.post(url=url, data=body, headers=headers, verify=False)
        return r
