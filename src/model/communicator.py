import asyncio

import requests
import json
import websockets

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode


def rest_communicator(func):
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)

            if response.status_code != 200:
                raise Exception("통신 에러가 발생했습니다.")

            return response.json()

        except Exception as e:
            print(e)

    return wrapper


class AuthComm:

    @rest_communicator
    def get_key(self, url: str, app_key: str, secret_key: str):
        headers = {
            "content-type": "application/json; utf-8"
        }

        data = {
            "grant_type": "client_credentials",
            "appkey": app_key,
            "secretkey": secret_key
        }

        return requests.post(url, headers=headers, data=json.dumps(data))

    @rest_communicator
    def get_token(self, url: str, app_key: str, secret_key: str):
        headers = None

        data = {
            "grant_type": "client_credentials",
            "appkey": app_key,
            "appsecret": secret_key
        }

        return requests.post(url=url, headers=headers, data=json.dumps(data))


class PrimaryStockComm:

    @rest_communicator
    def get_info(self, url: str, token: str, app_key: str, secret_key: str, tr_id: str):

        headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": token,
            "appkey": app_key,
            "appsecret": secret_key,
            "tr_id": "CTPF1002R",
            "tr_count": "",
            "custtype": "P"
        }

        params = {
            "PRDT_TYPE_CD": "300",
            "PDNO": "000660"
        }

        return requests.get(url=url, headers=headers, params=params)


class AccountComm:

    @rest_communicator
    def get_account(self, url: str, token: str, app_key: str, secret_key: str, accuont_num: str):
        headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": token,
            "appkey": app_key,
            "appsecret": secret_key,
            "tr_id": "TTTC8434R",
            "custtype": "P"
        }

        params = {
            "CANO": accuont_num.split("-")[0],
            "ACNT_PRDT_CD": accuont_num.split("-")[1],
            "AFHR_FLPR_YN": "N",
            'OFL_YN': 'N',
            'INQR_DVSN': '01',
            'UNPR_DVSN': '01',
            'FUND_STTL_ICLD_YN': 'N',
            'FNCG_AMT_AUTO_RDPT_YN': 'N',
            'PRCS_DVSN': '01',
            'CTX_AREA_FK100': "",
            'CTX_AREA_NK100': ""
        }

        return requests.get(url=url, headers=headers, params=params)


def aes_cbc_base64_dec(key, iv, cipher_text):
    """
    :param key:  str type AES256 secret key value
    :param iv: str type AES256 Initialize Vector
    :param cipher_text: Base64 encoded AES256 str
    :return: Base64-AES256 decodec str
    """
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    return bytes.decode(unpad(cipher.decrypt(b64decode(cipher_text)), AES.block_size))

async def realtime_trading_price_comm(url, approval_key: str, tr_key: str, ping_interval=None):
    async with websockets.connect(url, ping_interval=ping_interval) as websocket:

        data = {
            "header": {
                "approval_key": approval_key,
                "custtype": "P",
                "tr_type": "1",
                "content-type": "utf-8"
            },
            "body": {
                "input": {
                    "tr_id": "H0STCNT0",
                    "tr_key": tr_key
                }
            }
        }

        await websocket.send(json.dumps(data))
        await asyncio.sleep(0.5)

        print(f"Send data : {data}")

        while True:
            try:
                response = await websocket.recv()

                # output = json.loads(response[0])['body']['output']
                # iv = output['iv']
                # key = output['key']

                print(f"Recev Command is :{response.split('|')}")

            except websockets.ConnectionClosed:
                continue
