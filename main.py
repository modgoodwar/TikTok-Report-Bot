import os
from utils.api import Api
from random import choice
from threading import Thread, active_count
import time

class TikReport:
    def __init__(self, cookies: dict):
        self.cookies = cookies
        self.userInfo = None
        self.selfInfo = None
        self.reasons = ['9101','91011','9009','90093']

    def reportAccount(self):
        if not self.userInfo or not self.selfInfo:
            print("No user data")
            return

        for reason in self.reasons:
            try:
                params = {
                    'secUid': self.userInfo['userInfo']['user']['secUid'],
                    'nickname': self.userInfo['userInfo']['user']['nickname'],
                    'object_id': self.userInfo['userInfo']['user']['id'],
                    'owner_id': self.userInfo['userInfo']['user']['id'],
                    'target': self.userInfo['userInfo']['user']['id'],
                    'reporter_id': self.selfInfo['data']['user_id'],
                    'reason': reason,
                    'report_type': 'user',
                }

                req = Api(cookies=self.cookies).tiktok_request(
                    'aweme/v2/aweme/feedback/',
                    extra_params=params
                )

                print(f"request enviado: {reason}")

            except Exception as e:
                print(f"error: {e}")

    def start(self, username: str):
        try:
            self.userInfo = Api(cookies=self.cookies).user_info(username).json()
            self.selfInfo = Api(cookies=self.cookies).account_info().json()

            print("datos cargados")
            self.reportAccount()

        except Exception as e:
            print(f"error start: {e}")


if __name__ == "__main__":
    # VARIABLES DE ENTORNO (Railway)
    SESSION_ID = os.getenv("SESSION_ID")
    USERNAME = os.getenv("USERNAME")

    if not SESSION_ID or not USERNAME:
        print("Faltan variables de entorno")
        exit()

    cookies = {
        "sessionid": SESSION_ID
    }

    threads = 2  # ⚠️ bajo para evitar problemas

    bot = TikReport(cookies)
    bot.start(USERNAME)

    print("finalizado")
